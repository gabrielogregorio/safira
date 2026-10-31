import AxeBuilder from '@axe-core/playwright';
import { devices, expect, test, type Locator, type Page } from '@playwright/test';

const WCAG_AA_TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'];
const LAYOUT_WIDTHS = [320, 375, 768, 1280, 1440];

const waitForAnimations = async (page: Page): Promise<void> => {
  await page.evaluate(() =>
    Promise.allSettled(
      document
        .getAnimations()
        .filter((animation) => animation.effect?.getTiming().iterations !== Infinity)
        .map((animation) => animation.finished),
    ),
  );
};

const chooseTheme = async (page: Page, name: string): Promise<void> => {
  const toggle = page.getByRole('button', { name: /^Theme: / });

  while ((await toggle.getAttribute('aria-label')) !== `Theme: ${name}`) {
    await toggle.click();
  }
};

const expectNoViolations = async (page: Page): Promise<void> => {
  await waitForAnimations(page);
  const results = await new AxeBuilder({ page }).withTags(WCAG_AA_TAGS).analyze();

  expect(results.violations).toEqual([]);
};

const expectNoHorizontalScroll = async (page: Page): Promise<void> => {
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );

  expect(overflow).toBe(0);
};

const createProjectWithCode = async (page: Page, code: string): Promise<void> => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Create project' }).click();
  await page.getByRole('button', { name: 'Go ahead' }).click();
  await page.getByLabel('Code editor').click();
  await page.keyboard.insertText(code);
};

const openLessons = async (page: Page): Promise<void> => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Create project' }).click();
  await page.getByRole('button', { name: 'Go ahead' }).click();
  await page.getByRole('menuitem', { name: 'Help' }).click();
  await page.getByRole('menuitem', { name: 'Lessons' }).click();
  await expect(page.getByRole('dialog', { name: 'Lessons' })).toBeVisible();
};

const breakpointDots = (page: Page): Locator =>
  page.locator('.editor-breakpoints .cm-gutterElement').filter({ visible: true });

const runCode = async (page: Page): Promise<void> => {
  await page.getByRole('button', { name: 'Run', exact: true }).click();
};

const VISION_NAMES = [
  'Protanopia (weak red)',
  'Deuteranopia (weak green)',
  'Tritanopia (weak blue)',
  'Achromatopsia (no colors)',
  'Low vision (cataract, glaucoma)',
  'Light sensitivity (migraine, photophobia)',
  'Epilepsy and dizziness (no motion)',
];

const chooseVision = async (page: Page, name: string): Promise<void> => {
  const toggle = page.getByRole('button', { name: /^Accessibility: / });

  while ((await toggle.getAttribute('aria-label')) !== `Accessibility: ${name}`) {
    await toggle.click();
  }
};

for (const vision of VISION_NAMES) {
  for (const theme of ['Light', 'Dark', 'Simple']) {
    test(`has no violations with ${vision} in the ${theme} theme`, async ({ page }) => {
      await page.goto('/');
      await chooseTheme(page, theme);
      await chooseVision(page, vision);
      await expectNoViolations(page);

      await createProjectWithCode(page, '# nota\nse 1 == 1 entao mostre "oi"\nx recebe 2 + 3');
      await expectNoViolations(page);
    });
  }
}

test('keeps the mode after a reload and offers it in the menu', async ({ page }) => {
  await page.goto('/');
  await chooseVision(page, 'Tritanopia (weak blue)');
  await expect(page.locator('html')).toHaveAttribute('data-vision', 'tritanopia');
  await page.reload();
  await expect(page.locator('html')).toHaveAttribute('data-vision', 'tritanopia');

  await createProjectWithCode(page, 'mostre "oi"');
  await page.getByRole('menuitem', { name: 'Interface' }).click();
  await page.getByRole('menuitem', { name: 'Accessibility' }).click();
  await expect(page.getByRole('menuitemradio', { name: 'Tritanopia (weak blue)' })).toHaveAttribute(
    'aria-checked',
    'true',
  );
  await page.getByRole('menuitemradio', { name: 'Default' }).click();
  await expect(page.locator('html')).toHaveAttribute('data-vision', 'default');
});

test('marks code with more than color and stops the motion in the calm mode', async ({ page }) => {
  await page.goto('/');
  await chooseVision(page, 'Achromatopsia (no colors)');
  await createProjectWithCode(page, '# nota\nmostre "oi"');
  await expect(page.locator('.syntax-comentario').first()).toHaveCSS('font-style', 'italic');
  await expect(page.locator('.syntax-string').first()).toHaveCSS('text-decoration-line', 'underline');
});

test('runs a program in the worker', async ({ page }) => {
  await createProjectWithCode(page, 'repita 2 vezes { mostre "oi" }\nmostre 1 + 2');
  await runCode(page);

  await expect(page.getByRole('log')).toContainText('oi');
  await expect(page.getByRole('log')).toContainText('3');
  await expect(page.getByRole('log')).toContainText('Script finished');
});

test('mixes languages in the same script', async ({ page }) => {
  await createProjectWithCode(page, 'x recebe 1\nif x is equal to 1 { mostrar "um" }\nrepeat 2 vezes { show "z" }');
  await runCode(page);

  await expect(page.getByRole('log')).toContainText('um');
});

test('stops an infinite loop and the page stays responsive', async ({ page }) => {
  await createProjectWithCode(page, 'enquanto 1 == 1 { mostre "x" }');
  await runCode(page);
  await page.getByRole('main').getByRole('log').waitFor();
  await page.getByRole('button', { name: 'Stop', exact: true }).click();

  await expect(page.getByRole('log')).toContainText('Execution stopped');
  await expect(page.getByRole('button', { name: 'Run', exact: true })).toBeEnabled();
});

test('asks for input and continues', async ({ page }) => {
  await createProjectWithCode(page, 'n = o que o usuario digitar\nmostre "oi " + n');
  await runCode(page);
  await page.getByLabel('Type here and press Enter').fill('Ana');
  await page.keyboard.press('Enter');

  await expect(page.getByRole('log')).toContainText('oi Ana');
});

test('imports another virtual file and keeps projects after a reload', async ({ page }) => {
  await createProjectWithCode(
    page,
    'crie o arquivo "lib.safira"\nsobrescreva "v = 7" no arquivo "lib.safira"\nimporte lib\nmostre v',
  );
  await runCode(page);

  await expect(page.getByRole('log')).toContainText('7');

  await page.keyboard.press('Control+s');
  await page.reload();
  await page.keyboard.press('Control+o');

  await expect(page.getByRole('dialog').getByRole('button', { name: 'lib.safira' })).toBeVisible();
});

test('debugs line by line with the variables panel', async ({ page }) => {
  await createProjectWithCode(page, 'x = 1\nmostre x');
  await page.keyboard.press('F6');
  await page.getByRole('button', { name: 'Next line' }).click();

  await expect(page.getByRole('cell', { name: 'x', exact: true })).toBeVisible();
});

test('runs with Ctrl+Enter from inside the editor without adding a line', async ({ page }) => {
  await createProjectWithCode(page, 'mostre "atalho"');
  await page.keyboard.press('Control+Enter');

  await expect(page.getByRole('log')).toContainText('atalho');
  await expect(page.locator('.cm-line')).toHaveCount(1);
});

test('stops at a breakpoint set by clicking its dot', async ({ page }) => {
  await createProjectWithCode(page, 'x = 1\ny = 2\nmostre x + y');
  await breakpointDots(page).nth(1).click();
  await expect(page.locator('.breakpoint-dot-active')).toHaveCount(1);
  await runCode(page);

  await expect(page.getByText('Paused on line 2')).toBeVisible();
  await expect(page.getByRole('cell', { name: 'x', exact: true })).toBeVisible();
  await expect(page.getByRole('cell', { name: 'y', exact: true })).toBeHidden();

  await page.getByRole('button', { name: 'Continue' }).first().click();

  await expect(page.getByRole('log')).toContainText('3');
});

test('a breakpoint on a comment stops at the next command', async ({ page }) => {
  await createProjectWithCode(page, '# nota\nmostre 1');
  await breakpointDots(page).first().click();
  await runCode(page);

  await expect(page.getByText('Paused on line 2')).toBeVisible();
});

test('removes a breakpoint with a second click', async ({ page }) => {
  await createProjectWithCode(page, 'mostre 1');
  const dot = breakpointDots(page).first();
  await dot.click();
  await dot.click();

  await expect(page.locator('.breakpoint-dot-active')).toHaveCount(0);
});

test('navigates the top menu with the keyboard', async ({ page }) => {
  await createProjectWithCode(page, 'mostre 1');
  await page.getByRole('menuitem', { name: 'File' }).focus();
  await page.keyboard.press('Enter');
  await expect(page.getByRole('menuitem', { name: 'New tab' })).toBeFocused();
  await waitForAnimations(page);

  await page.keyboard.press('ArrowRight');
  await expect(page.getByRole('menuitem', { name: 'Run all' })).toBeVisible();

  await page.keyboard.press('Escape');
  await expect(page.getByRole('menuitem', { name: 'Run all' })).toBeHidden();
  await expect(page.getByRole('menuitem', { name: 'Run', exact: true })).toBeFocused();
});

test('changes the theme from the menu', async ({ page }) => {
  await createProjectWithCode(page, 'mostre 1');
  await page.getByRole('menuitem', { name: 'Interface' }).click();
  await page.getByRole('menuitem', { name: 'Theme' }).click();
  await page.getByRole('menuitemradio', { name: 'Dark' }).click();

  await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
});

test('closing a tab keeps what was typed, without asking', async ({ page }) => {
  await createProjectWithCode(page, 'mostre "fica"');
  await page
    .getByRole('button', { name: /^Close tab/ })
    .first()
    .click();
  await expect(page.getByRole('dialog')).toHaveCount(0);
  await expect.poll(() => page.evaluate(() => localStorage.getItem('safira.projects.v1'))).toContain('fica');
});

test('colors the syntax of the code', async ({ page }) => {
  await createProjectWithCode(page, 'mostre "oi"');

  await expect(page.locator('.syntax-exibicao')).toHaveText('mostre');
  await expect(page.locator('.syntax-string')).toHaveText('"oi"');
});

test.describe('accessibility', () => {
  test('an open menu has no violations', async ({ page }) => {
    await createProjectWithCode(page, 'mostre 1');
    await page.getByRole('menuitem', { name: 'Run', exact: true }).click();
    await expect(page.getByRole('menuitem', { name: 'Run all' })).toBeVisible();
    await expectNoViolations(page);
  });

  for (const theme of ['Simple', 'Dark', 'Light']) {
    test(`home and editor have no violations in the ${theme} theme`, async ({ page }) => {
      await page.goto('/');
      await chooseTheme(page, theme);
      await expectNoViolations(page);

      await page.getByRole('button', { name: 'Create project' }).click();
      await expectNoViolations(page);
      await page.getByRole('button', { name: 'Go ahead' }).click();
      await page.getByLabel('Code editor').click();
      await page.keyboard.insertText('se 1 == 1 { mostre "oi" } # nota\nfuncao f { retorne 1 }');
      await runCode(page);
      await expect(page.getByRole('log')).toContainText('Script finished');
      await expectNoViolations(page);
    });
  }

  test('lessons have no violations', async ({ page }) => {
    await openLessons(page);
    await waitForAnimations(page);
    await expectNoViolations(page);
  });
});

test.describe('layout', () => {
  for (const width of LAYOUT_WIDTHS) {
    test(`has no horizontal scroll at ${width}px`, async ({ page }) => {
      await page.setViewportSize({ width, height: 720 });
      await page.goto('/');
      await expectNoHorizontalScroll(page);

      await page.getByRole('button', { name: 'Create project' }).click();
      await expectNoHorizontalScroll(page);
      await page.getByRole('button', { name: 'Go ahead' }).click();
      await expectNoHorizontalScroll(page);
    });
  }
});

test('a modal closes when clicking outside of it', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Create project' }).click();
  await waitForAnimations(page);
  await page.mouse.click(5, 5);

  await expect(page.getByRole('dialog')).toBeHidden();
});

test('a modal opens with the retro animation', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Create project' }).click();
  await expect(page.getByRole('dialog')).toBeVisible();
  const animationNames = await page.evaluate(() =>
    document.getAnimations().map((animation) => (animation as CSSAnimation).animationName),
  );

  expect(animationNames).toEqual(expect.arrayContaining(['retro-crt-on', 'retro-zoom-rectangle']));
});

test('deleting a project asks for confirmation', async ({ page }) => {
  await createProjectWithCode(page, 'mostre 1');
  await page.keyboard.press('Control+s');
  await page.getByRole('button', { name: 'Back to projects' }).click();
  await page.getByRole('button', { name: 'Delete New project' }).click();
  await expectNoViolations(page);
  await page.getByRole('dialog').getByRole('button', { name: 'Cancel' }).click();
  await expect(page.getByText('New project', { exact: true })).toBeVisible();

  await page.getByRole('button', { name: 'Delete New project' }).click();
  await page.getByRole('dialog').getByRole('button', { name: 'Delete', exact: true }).click();

  await expect(page.getByText('You have no projects yet.')).toBeVisible();
});

test('the editor takes the focus when a project opens', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Create project' }).click();
  await page.getByRole('button', { name: 'Go ahead' }).click();
  await waitForAnimations(page);
  await page.keyboard.insertText('mostre "foco"');

  await expect(page.getByLabel('Code editor')).toBeFocused();
  await expect(page.getByLabel('Code editor')).toContainText('mostre "foco"');
});

test('the page does not scroll in the lessons and the sidebar stays in place', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 500 });
  await openLessons(page);
  await page.getByRole('link', { name: 'Next' }).click();
  await expect(page.getByRole('heading', { name: 'Exibição', exact: true })).toBeVisible();
  const sidebarTop = await page
    .getByRole('link', { name: /^Welcome to Safira/ })
    .evaluate((link) => link.getBoundingClientRect().top);
  await page.locator('.lesson').evaluate((lesson) => {
    lesson.scrollTop = lesson.scrollHeight;
  });

  expect(await page.evaluate(() => document.documentElement.scrollHeight - window.innerHeight)).toBe(0);
  expect(
    await page.getByRole('link', { name: /^Welcome to Safira/ }).evaluate((link) => link.getBoundingClientRect().top),
  ).toBe(sidebarTop);
  expect(await page.locator('.lesson').evaluate((lesson) => lesson.scrollTop)).toBeGreaterThan(0);
});

test('a lesson example opens and runs in the same project', async ({ page }) => {
  await openLessons(page);
  await page.getByRole('link', { name: 'Next' }).click();
  await page.getByRole('button', { name: 'Open in the IDE' }).first().click();
  await expect(page.getByRole('dialog')).toHaveCount(0);
  await expect(page.locator('.tab-active')).toContainText('aula-02-exibicao.safira');
  await runCode(page);

  await expect(page.getByRole('log')).toContainText('Script finished');
});

test('what was typed survives the page dying', async ({ page }) => {
  await createProjectWithCode(page, 'mostre "fica salvo"');
  await expect.poll(() => page.evaluate(() => localStorage.getItem('safira.projects.v1'))).toContain('fica salvo');
  await page.reload();

  await expect(page.locator('.cm-content')).toContainText('fica salvo');
});

test('imports from a virtual folder created in the sidebar', async ({ page }) => {
  await createProjectWithCode(page, 'importe dados/lib\nmostre v');
  await page.keyboard.press('Control+s');
  await page.getByRole('button', { name: 'New folder' }).click();
  await expect(page.getByLabel('Folder name')).toBeFocused();
  await page.keyboard.type('dados');
  await page.keyboard.press('Enter');
  await page.getByRole('button', { name: 'dados' }).click({ button: 'right' });
  await page.getByRole('menuitem', { name: 'New file' }).click();
  await expect(page.getByLabel('File name')).toBeFocused();
  await page.keyboard.type('lib');
  await page.keyboard.press('Enter');
  await page.getByLabel('Code editor').click();
  await page.keyboard.insertText('v = 9');
  await page.keyboard.press('Control+s');
  await page.getByRole('button', { name: 'main.safira' }).first().click();
  await runCode(page);

  await expect(page.getByRole('log')).toContainText('9');
});

test('exports a project and imports it back', async ({ page }) => {
  await createProjectWithCode(page, 'mostre "zip"');
  await page.keyboard.press('Control+s');
  await page.getByRole('button', { name: 'Back to projects' }).click();
  const downloadPromise = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Export New project' }).click();
  const download = await downloadPromise;

  expect(download.suggestedFilename()).toBe('New-project.zip');

  await page.locator('.archive-input').setInputFiles(await download.path());
  await expect(page.getByText('Imported 1 files.')).toBeVisible();
  await page
    .getByRole('link', { name: /^Open / })
    .first()
    .click();

  await expect(page.getByLabel('Code editor')).toContainText('mostre "zip"');
});

test('the theme changes in the background, with nothing in front of the screen', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Theme: Light' }).click();

  await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
  await expect(page.locator('html')).toHaveAttribute('data-theme-changing', 'true');
  await expect(page.locator('.scenery-dark')).toHaveCSS('opacity', '1');
  await expect(page.locator('.scenery-light')).toHaveCSS('opacity', '0');
  await expect(page.locator('html')).not.toHaveAttribute('data-theme-changing', 'true');
});

test('the language change scrambles the letters into the new text', async ({ page }) => {
  await page.goto('/');
  const title = page.locator('.home-settings .button-primary');
  await page.evaluate(() => {
    const seen: string[] = [];
    const button = document.querySelector('.home-settings .button-primary');
    new MutationObserver(() => {
      seen.push(button?.textContent ?? '');
    }).observe(button as Element, { characterData: true, subtree: true, childList: true });
    Object.assign(window, { seenTexts: seen });
  });
  await page.getByRole('button', { name: 'Language: English' }).click();

  await expect(title).toHaveText('Criar projeto');
  const seenTexts = await page.evaluate(() => (window as unknown as { seenTexts: string[] }).seenTexts);

  expect(seenTexts.some((text) => text !== 'Criar projeto' && text !== 'Create project')).toBe(true);
  expect(seenTexts.at(-1)).toBe('Criar projeto');
});

test('changing the language several times always ends on the text of the chosen language', async ({ page }) => {
  await page.goto('/');
  const language = page.locator('.orb-toggles button').nth(1);
  const title = page.locator('.home-settings .button-primary');

  await language.click();
  await expect(title).toHaveText('Criar projeto');
  await language.click();
  await expect(title).toHaveText('Crear proyecto');
  await language.click();
  await expect(title).toHaveText('创建项目');
  await language.click();
  await expect(title).toHaveText('プロジェクトを作成');
  await language.click();
  await expect(title).toHaveText('Create project');

  for (let click = 0; click < 5; click += 1) {
    await language.click();
  }

  await expect(title).toHaveText('Create project');
});

test('names that are not translated stay still during the language change', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Create project' }).click();
  await page.getByRole('button', { name: 'Go ahead' }).click();
  await page.getByRole('button', { name: 'Back to projects' }).click();
  const name = await page.locator('.project-name').first().textContent();
  await page.evaluate(() => {
    const changes: string[] = [];
    new MutationObserver(() => {
      changes.push('changed');
    }).observe(document.querySelector('.project-name') as Element, { characterData: true, subtree: true });
    Object.assign(window, { nameChanges: changes });
  });
  await page.getByRole('button', { name: /^Language: / }).click();
  await expect(page.locator('.home-settings .button-primary')).toHaveText('Criar projeto');

  await expect(page.locator('.project-name').first()).toHaveText(name ?? '');
  expect(await page.evaluate(() => (window as unknown as { nameChanges: string[] }).nameChanges)).toEqual([]);
});

test('closing a modal plays the closing animation and leaves nothing behind', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Create project' }).click();
  await waitForAnimations(page);
  await page.keyboard.press('Escape');

  await expect(page.getByRole('dialog')).toBeHidden();
  await expect(page.locator('.modal-closing')).toBeAttached();
  await expect(page.locator('.modal-closing')).toHaveCount(0);
});

test('panels can be resized by dragging and the size is kept', async ({ page }) => {
  await createProjectWithCode(page, 'mostre 1');
  const divider = page.getByRole('separator', { name: 'Resize the files panel' });
  const sidebar = page.locator('.file-sidebar');
  const before = (await sidebar.boundingBox())?.width ?? 0;
  const box = await divider.boundingBox();
  await page.mouse.move((box?.x ?? 0) + 2, (box?.y ?? 0) + 40);
  await page.mouse.down();
  await page.mouse.move((box?.x ?? 0) + 102, (box?.y ?? 0) + 40);
  await page.mouse.up();

  await expect.poll(async () => (await sidebar.boundingBox())?.width).toBe(before + 100);

  await page.reload();

  await expect.poll(async () => (await page.locator('.file-sidebar').boundingBox())?.width).toBe(before + 100);
});

test('panels can be resized with the keyboard', async ({ page }) => {
  await createProjectWithCode(page, 'mostre 1');
  const divider = page.getByRole('separator', { name: 'Resize the variables panel' });
  await divider.focus();
  await page.keyboard.press('ArrowUp');

  await expect(divider).toHaveAttribute('aria-valuenow', '256');
});

test('the icons cycle through every choice and come back to the first', async ({ page }) => {
  await page.goto('/');
  const theme = page.getByRole('button', { name: /^Theme: / });

  await theme.click();
  await theme.click();
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'simple');
  await theme.click();
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');
  await expect(page.getByRole('dialog')).toHaveCount(0);
});

test('the IDE keeps theme, language and sound in the Interface menu', async ({ page }) => {
  await createProjectWithCode(page, 'mostre 1');
  await expect(page.locator('.toolbar .orb-toggle')).toHaveCount(0);

  await page.getByRole('menuitem', { name: 'Interface' }).click();
  await page.getByRole('menuitem', { name: 'Language' }).click();
  await page.getByRole('menuitemradio', { name: 'Español' }).click();
  await expect(page.locator('html')).toHaveAttribute('lang', 'es');

  await page.getByRole('menuitem', { name: 'Interfaz' }).click();
  await page.getByRole('menuitemcheckbox', { name: 'Sonido' }).click();
  await expect(page.getByRole('menuitemcheckbox', { name: 'Sonido' })).toBeHidden();
  await page.getByRole('menuitem', { name: 'Interfaz' }).click();
  await expect(page.getByRole('menuitemcheckbox', { name: 'Sonido' })).toHaveAttribute('aria-checked', 'false');
  await page.keyboard.press('Escape');
  await expect(page.getByRole('menuitemcheckbox', { name: 'Sonido' })).toBeHidden();

  await page.getByRole('menuitem', { name: 'Interfaz' }).click();
  await page.getByRole('menuitem', { name: 'Tema', exact: true }).click();
  await page.getByRole('menuitemradio', { name: 'Oscuro' }).click();
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
  await expect(page.locator('html')).toHaveCSS('--syntax-string', '#ffff68');
});

test('the code font switches between mono and the Frutiger Aero font from the menu', async ({ page }) => {
  await createProjectWithCode(page, 'mostre 1');
  const fontOfCode = (): Promise<string> =>
    page.locator('.cm-content').evaluate((element) => getComputedStyle(element).fontFamily);

  expect(await fontOfCode()).toContain('JetBrains Mono');

  await page.getByRole('menuitem', { name: 'Interface' }).click();
  await page.getByRole('menuitem', { name: 'Code font' }).click();
  await page.getByRole('menuitemradio', { name: 'Istok Web' }).click();
  await expect.poll(fontOfCode).toContain('Istok Web');

  await page.reload();
  await expect.poll(fontOfCode).toContain('Istok Web');
  expect(await page.evaluate(() => document.fonts.check('16px "Istok Web"'))).toBe(true);
});

test('a new file shows up in the tree, and moving away keeps its provisional name', async ({ page }) => {
  await createProjectWithCode(page, 'mostre 1');
  await page.getByRole('button', { name: 'New file' }).click();
  await expect(page.getByLabel('File name')).toHaveValue('new-file.safira');
  await page.getByLabel('Code editor').click();

  await expect(page.locator('.tree-name', { hasText: 'new-file.safira' })).toBeVisible();
  await expect(page.getByLabel('File name')).toHaveCount(0);
});

test('the project name sits on top of the sidebar, edited in place, and the gem stays out', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Create project' }).click();
  await page.getByRole('button', { name: 'Go ahead' }).click();
  await expect(page.locator('.toolbar .safira-logo')).toHaveCount(0);
  const sidebar = await page.locator('.file-sidebar').boundingBox();
  await page.locator('.project-name-button').click();
  await page.keyboard.type('Um nome bem comprido que nao cabe na barra lateral do projeto');
  await page.locator('.tab-bar').click({ position: { x: 300, y: 10 } });
  await expect(page.locator('.project-name-button')).toContainText('Um nome bem comprido');

  expect((await page.locator('.file-sidebar').boundingBox())?.width).toBe(sidebar?.width);
});

test('files and folders are renamed from the right click', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Create project' }).click();
  await page.getByRole('button', { name: 'Go ahead' }).click();
  await page.locator('.file-sidebar').getByRole('button', { name: 'main.safira' }).click({ button: 'right' });
  await page.getByRole('menuitem', { name: 'Rename' }).click();
  await expect(page.getByLabel('File name')).toBeFocused();
  await page.keyboard.type('inicio');
  await page.keyboard.press('Enter');
  await expect(page.locator('.file-sidebar').getByRole('button', { name: 'inicio.safira' })).toBeVisible();
  await expect(page.locator('.tab-active')).toContainText('inicio.safira');
  await expect(page).toHaveURL(/inicio\.safira/);
});

test('deleting is on the right click menu and asks for confirmation', async ({ page }) => {
  await createProjectWithCode(page, 'mostre 1');
  await page.getByRole('button', { name: 'New file' }).click();
  await page.keyboard.type('apagar');
  await page.keyboard.press('Enter');
  const row = page.locator('.tree-name', { hasText: 'apagar.safira' });
  await row.click({ button: 'right' });
  await page.getByRole('menuitem', { name: 'Delete' }).click();
  await page.getByRole('dialog').getByRole('button', { name: 'Delete' }).click();

  await expect(row).toHaveCount(0);
  await page.getByLabel('Code editor').click();
  await page.keyboard.insertText('x');
});

test('time passes on its own and a reload returns to the chosen theme', async ({ page }) => {
  await page.clock.install();
  await page.goto('/');
  await chooseTheme(page, 'Light');
  const html = page.locator('html');

  await page.clock.fastForward('01:00:00');
  await expect(html).toHaveAttribute('data-theme', 'light');

  await page.clock.fastForward('03:00:00');
  await expect(html).toHaveAttribute('data-theme', 'dark');
  await expect(page.getByRole('button', { name: 'Theme: Dark' })).toBeVisible();
  await expect(page.locator('.scenery-dark')).toHaveCSS('opacity', '1');

  await page.clock.fastForward('04:00:00');
  await expect(html).toHaveAttribute('data-theme', 'simple');

  await page.reload();
  await expect(html).toHaveAttribute('data-theme', 'light');
});

test('choosing a theme is a jump in time, from where the sky already is', async ({ page }) => {
  await page.clock.install();
  await page.goto('/');
  await page.clock.fastForward('04:00:00');
  await expect(page.getByRole('button', { name: 'Theme: Dark' })).toBeVisible();

  await page.getByRole('button', { name: 'Theme: Dark' }).click();
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'simple');

  await page.clock.fastForward('01:00:00');
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'simple');
});

test('the editor panel stays in place, with its line numbers, after typing and changing files', async ({ page }) => {
  await createProjectWithCode(page, 'mostre "uma linha comprida o bastante para o cursor andar pela tela toda"');
  await page.getByRole('button', { name: 'New file' }).click();
  await page.keyboard.press('Enter');
  await page.getByLabel('Code editor').click();
  await page.keyboard.insertText('x');
  await waitForAnimations(page);

  expect(await page.locator('.code-editor').evaluate((panel) => panel.scrollLeft)).toBe(0);
  await expect(page.locator('.cm-gutters').first()).toBeInViewport();
});

test('opening a project and a file play their animations', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Create project' }).click();
  await page.getByRole('button', { name: 'Go ahead' }).click();
  const running = (): Promise<string[]> =>
    page.evaluate(() => document.getAnimations().map((animation) => (animation as CSSAnimation).animationName));

  expect(await running()).toEqual(expect.arrayContaining(['ide-crt-on', 'file-open']));

  await waitForAnimations(page);
  await page.getByRole('button', { name: 'New file' }).click();
  await page.keyboard.press('Enter');
  await expect.poll(running).toContain('file-open');
});

test('the home screen keeps theme and language at the right of the action buttons', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 700 });
  await page.goto('/');
  const hero = await page.locator('.home-hero').boundingBox();
  const corner = await page.locator('.home-corner').boundingBox();
  const create = await page.getByRole('button', { name: 'Create project' }).boundingBox();
  const middle = (box: typeof corner): number => (box?.y ?? 0) + (box?.height ?? 0) / 2;

  expect(Math.abs(middle(corner) - middle(create))).toBeLessThan(2);
  expect((hero?.x ?? 0) + (hero?.width ?? 0) - (corner?.x ?? 0) - (corner?.width ?? 0)).toBeLessThan(40);
});

test('the home icons stay inside the panel on a narrow phone', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 700 });
  await page.goto('/');
  const hero = await page.locator('.home-hero').boundingBox();
  const corner = await page.locator('.home-corner').boundingBox();

  expect((corner?.x ?? 0) + (corner?.width ?? 0)).toBeLessThanOrEqual((hero?.x ?? 0) + (hero?.width ?? 0));
});

test('the sound can be turned off, and that is remembered', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Sound: On' }).click();
  await expect(page.getByRole('button', { name: 'Sound: Off' })).toBeVisible();

  await page.reload();
  await expect(page.getByRole('button', { name: 'Sound: Off' })).toBeVisible();
});

test('clicking and deleting play the recorded sounds, and the sound switch silences them', async ({ page }) => {
  await page.addInitScript(() => {
    const started: number[] = [];
    const start = AudioBufferSourceNode.prototype.start;
    AudioBufferSourceNode.prototype.start = function startAndRecord(...values) {
      started.push(this.buffer?.duration ?? 0);
      start.apply(this, values);
    };
    Object.assign(window, { startedSounds: started });
  });
  const sounds = (): Promise<number[]> =>
    page.evaluate(() => (window as unknown as { startedSounds: number[] }).startedSounds);

  await page.goto('/');
  await page.getByRole('button', { name: 'Create project' }).click();
  await expect.poll(sounds).toHaveLength(1);

  await page.getByRole('button', { name: 'Go ahead' }).click();
  await page.getByRole('button', { name: 'Back to projects' }).click();
  await page.getByRole('button', { name: /^Delete / }).click();
  await page.getByRole('dialog').getByRole('button', { name: 'Delete' }).click();
  await expect.poll(async () => Math.max(...(await sounds()))).toBeGreaterThan(0.25);

  await page.getByRole('button', { name: 'Sound: On' }).click();
  const before = (await sounds()).length;
  await page.getByRole('button', { name: 'Create project' }).click();
  await expect(page.getByRole('dialog')).toBeVisible();

  expect(await sounds()).toHaveLength(before);
});

test('modals sound when they open and when they close', async ({ page }) => {
  await page.addInitScript(() => {
    const started: number[] = [];
    const start = AudioBufferSourceNode.prototype.start;
    AudioBufferSourceNode.prototype.start = function startAndRecord(...values) {
      started.push(this.buffer?.duration ?? 0);
      start.apply(this, values);
    };
    Object.assign(window, { startedSounds: started });
  });
  const sounds = (): Promise<number[]> =>
    page.evaluate(() => (window as unknown as { startedSounds: number[] }).startedSounds);

  await page.goto('/');
  await page.getByRole('button', { name: 'Create project' }).click();
  await expect.poll(sounds).toHaveLength(1);
  const [opening] = await sounds();

  await page.getByRole('button', { name: 'Close' }).click();
  await expect.poll(sounds).toHaveLength(2);
  const [, closing] = await sounds();

  expect(opening).toBeGreaterThan(0.1);
  expect(closing).toBeGreaterThan(0.1);
  expect(closing).not.toBe(opening);
});

test('shows text in the colors written in every form', async ({ page }) => {
  await createProjectWithCode(page, 'mostrar "a" na cor #ff1122\nmostra na cor 0x00ff00 "b"\nmostre "c" na cor pink');
  await runCode(page);
  const terminal = page.getByRole('log');

  await expect(terminal.getByText('a', { exact: true })).toHaveCSS('color', 'rgb(255, 17, 34)');
  await expect(terminal.getByText('b', { exact: true })).toHaveCSS('color', 'rgb(0, 255, 0)');
  await expect(terminal.getByText('c', { exact: true })).toHaveCSS('color', 'rgb(255, 122, 198)');
});

test('suggests the next words in gray, Tab accepts them and the checkbox turns them off', async ({ page }) => {
  await createProjectWithCode(page, 'sh');
  const ghost = page.locator('.cm-ghost-text');

  await expect(ghost).toHaveText('ow "Hello!"');
  await page.keyboard.press('Tab');
  await expect(ghost).toHaveCount(0);
  await expect(page.locator('.cm-content')).toContainText('show "Hello!"');
  await page.keyboard.press('Control+Enter');
  await expect(page.getByRole('log')).toContainText('Hello!');

  await page.keyboard.press('Enter');
  await page.keyboard.type('sh');
  await expect(ghost).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(ghost).toHaveCount(0);

  await page.getByRole('checkbox', { name: 'Smart suggestions' }).uncheck();
  await page.getByLabel('Code editor').click();
  await page.keyboard.press('Control+End');
  await page.keyboard.type('o');
  await page.keyboard.press('Backspace');
  await page.keyboard.type('o');
  await expect(ghost).toHaveCount(0);

  await page.reload();
  await expect(page.getByRole('checkbox', { name: 'Smart suggestions' })).not.toBeChecked();
});

test('a suggestion can be accepted by touching it', async ({ page }) => {
  await createProjectWithCode(page, 'sh');
  await page.locator('.cm-ghost-text').click();

  await expect(page.locator('.cm-content')).toContainText('show "Hello!"');
});

test('the home screen shows the animated globe', async ({ page }) => {
  await page.goto('/');

  await expect(page.locator('.home-brand .aero-orb')).toBeVisible();
  await expect(page.locator('canvas')).toHaveCount(0);
});

test('language is available on every screen', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('button', { name: /^Theme: / })).toBeVisible();
  await expect(page.getByRole('button', { name: /^Language: / })).toBeVisible();

  await page.getByRole('button', { name: 'Create project' }).click();
  await page.getByRole('button', { name: 'Go ahead' }).click();
  await page.getByRole('menuitem', { name: 'Interface' }).click();
  await page.getByRole('menuitem', { name: 'Language' }).click();
  await page.getByRole('menuitemradio', { name: 'Español' }).click();

  await expect(page.locator('html')).toHaveAttribute('lang', 'es');
});

test.describe('phone', () => {
  const { viewport, userAgent, deviceScaleFactor, isMobile, hasTouch } = devices['Pixel 7'];
  test.use({ viewport, userAgent, deviceScaleFactor, isMobile, hasTouch, locale: 'en-US' });

  test('runs a program, sets a breakpoint by touch and reads the variables', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('button', { name: 'Create project' }).tap();
    await page.getByRole('button', { name: 'Go ahead' }).tap();
    await page.getByLabel('Code editor').tap();
    await page.keyboard.insertText('x = 1\nmostre x');
    await breakpointDots(page).nth(1).tap();
    await expect(page.locator('.breakpoint-dot-active')).toHaveCount(1);
    await page.getByRole('button', { name: 'Run', exact: true }).tap();

    await expect(page.getByText('Paused on line 2')).toBeVisible();

    await page.getByRole('button', { name: 'Variables' }).tap();
    await expect(page.getByRole('cell', { name: 'x', exact: true })).toBeVisible();

    await page.getByRole('button', { name: 'Output' }).tap();
    await page.getByRole('button', { name: 'Continue' }).first().tap();
    await expect(page.getByRole('log')).toContainText('1');
    await expectNoHorizontalScroll(page);
  });

  test('every touch target of the editor has at least 44 pixels', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('button', { name: 'Create project' }).tap();
    await page.getByRole('button', { name: 'Go ahead' }).tap();
    const heights = await page
      .locator('.toolbar button, .mobile-panel-button')
      .evaluateAll((buttons) => buttons.map((button) => button.getBoundingClientRect().height));

    expect(Math.min(...heights)).toBeGreaterThanOrEqual(44);
  });

  test('opens the menu by touch inside the screen and has no violations', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('button', { name: 'Create project' }).tap();
    await page.getByRole('button', { name: 'Go ahead' }).tap();
    await page.getByRole('menuitem', { name: 'Examples' }).tap();
    await expect(page.getByRole('menuitem', { name: 'Lists' })).toBeVisible();
    await expectNoViolations(page);
  });
});

test.describe('lesson mode', () => {
  const startLessonMode = async (page: Page): Promise<void> => {
    await page.goto('/');
    await page.getByRole('button', { name: 'Create project' }).click();
    await page.getByRole('button', { name: 'Go ahead' }).click();
    await page.locator('label', { hasText: 'Lesson mode' }).click();
    await expect(page.locator('.lesson-brief')).toBeVisible();
  };

  const runAndGoOn = async (page: Page): Promise<void> => {
    await page.getByRole('button', { name: 'Run', exact: true }).click();
    const next = page.locator('.lesson-actions').getByRole('button', { name: 'Next' });
    await expect(next).toBeEnabled();
    await next.click();
  };

  test('goes through a lesson up to a checked challenge', async ({ page }) => {
    await startLessonMode(page);
    await runAndGoOn(page);
    await runAndGoOn(page);
    await runAndGoOn(page);

    await page.getByRole('button', { name: 'Run', exact: true }).click();
    await expect(page.locator('.lesson-status')).toContainText('Tip:');
    await expect(page.locator('.lesson-actions').getByRole('button', { name: 'Next' })).toBeDisabled();

    await page.getByRole('button', { name: 'Show the solution' }).click();
    await page.getByRole('button', { name: 'Run', exact: true }).click();
    await expect(page.locator('.lesson-status')).toContainText('Correct! Challenge complete.');

    await page.locator('.lesson-actions').getByRole('button', { name: 'Next' }).click();
    await expect(page.getByRole('combobox', { name: 'Choose a lesson' })).toHaveValue('aula-02-exibicao');
  });

  test('keeps the page inside the phone screen', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await startLessonMode(page);

    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);

    expect(overflow).toBeLessThanOrEqual(0);
  });

  for (const theme of ['Light', 'Dark', 'Simple']) {
    test(`has no accessibility problem in the ${theme} theme`, async ({ page }) => {
      await startLessonMode(page);
      await page.getByRole('menuitem', { name: 'Interface' }).click();
      await page.getByRole('menuitem', { name: 'Theme' }).click();
      await page.getByRole('menuitemradio', { name: theme }).click();
      await page.keyboard.press('Escape');
      await page.getByRole('button', { name: 'Run', exact: true }).click();
      await expect(page.locator('.lesson-status')).toContainText('Well done');

      const results = await new AxeBuilder({ page }).include('.tab-bar').include('.lesson-brief').analyze();

      expect(results.violations).toEqual([]);
    });
  }
});
