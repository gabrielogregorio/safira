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

const breakpointDots = (page: Page): Locator =>
  page.locator('.editor-breakpoints .cm-gutterElement').filter({ visible: true });

const runCode = async (page: Page): Promise<void> => {
  await page.getByRole('button', { name: 'Run', exact: true }).click();
};

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
  await expect(page.getByRole('menuitem', { name: 'Open file' })).toBeFocused();
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

test('asks before closing a tab with unsaved work', async ({ page }) => {
  await createProjectWithCode(page, 'mostre 1');
  await page.getByRole('button', { name: 'Close tab main.safira' }).click();

  await expect(page.getByRole('dialog', { name: 'Do you want to save your program?' })).toBeVisible();
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
    await page.goto('/');
    await page.getByRole('button', { name: 'Lessons' }).click();
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
  await page.goto('/#/lessons/aula-02-exibicao');
  const sidebarTop = await page
    .getByRole('link', { name: /^Apresentação/ })
    .evaluate((link) => link.getBoundingClientRect().top);
  await page.locator('.lesson').evaluate((lesson) => {
    lesson.scrollTop = lesson.scrollHeight;
  });

  expect(await page.evaluate(() => document.documentElement.scrollHeight - window.innerHeight)).toBe(0);
  expect(
    await page.getByRole('link', { name: /^Apresentação/ }).evaluate((link) => link.getBoundingClientRect().top),
  ).toBe(sidebarTop);
  expect(await page.locator('.lesson').evaluate((lesson) => lesson.scrollTop)).toBeGreaterThan(0);
});

test('a lesson example opens and runs in the IDE', async ({ page }) => {
  await page.goto('/#/lessons/aula-02-exibicao');
  await page.getByRole('button', { name: 'Open in the IDE' }).first().click();
  await runCode(page);

  await expect(page.getByRole('log')).toContainText('Script finished');
});

test('recovers unsaved work after the page dies', async ({ page }) => {
  await createProjectWithCode(page, 'mostre "nao salvo"');
  await expect.poll(() => page.evaluate(() => localStorage.getItem('safira.drafts.v1'))).toContain('nao salvo');
  await page.reload();

  await expect(page.getByText('Your unsaved work was recovered.')).toBeVisible();
  await expect(page.getByLabel('Code editor')).toContainText('mostre "nao salvo"');
});

test('imports from a virtual folder created in the sidebar', async ({ page }) => {
  await createProjectWithCode(page, 'importe dados/lib\nmostre v');
  await page.keyboard.press('Control+s');
  await page.getByRole('button', { name: 'New folder' }).click();
  await page.getByLabel('Folder name').fill('dados');
  await page.keyboard.press('Enter');
  await page.getByRole('button', { name: 'New file in dados' }).click();
  await page.getByLabel('File name').fill('lib');
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

  expect(new Set(seenTexts).size).toBeGreaterThan(3);
  expect(seenTexts.at(-1)).toBe('Criar projeto');
});

test('changing the language several times always ends on the text of the chosen language', async ({ page }) => {
  await page.goto('/');
  const language = page.locator('.orb-toggles button').last();
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

test('the IDE starts with the language icon and leaves the theme to the Interface menu', async ({ page }) => {
  await createProjectWithCode(page, 'mostre 1');
  const toolbar = page.locator('.toolbar');

  await expect(toolbar.locator('> :first-child')).toHaveAttribute('aria-label', 'Language: English');
  await expect(page.getByRole('button', { name: /^Theme: / })).toHaveCount(0);
});

test('the home screen keeps theme and language in the top right corner, also on a narrow phone', async ({ page }) => {
  for (const width of [1280, 320]) {
    await page.setViewportSize({ width, height: 700 });
    await page.goto('/');
    const hero = await page.locator('.home-hero').boundingBox();
    const corner = await page.locator('.home-corner').boundingBox();
    const brand = await page.locator('.home-brand').boundingBox();

    expect(corner?.y).toBe(brand?.y);
    expect((corner?.x ?? 0) + (corner?.width ?? 0)).toBeLessThanOrEqual((hero?.x ?? 0) + (hero?.width ?? 0));
    expect((hero?.x ?? 0) + (hero?.width ?? 0) - (corner?.x ?? 0) - (corner?.width ?? 0)).toBeLessThan(40);
  }
});

test('the logo is a live 3D gem', async ({ page }) => {
  await page.goto('/');
  await page.mouse.move(900, 300);

  await expect(page.locator('canvas.safira-logo')).toBeVisible();
  await expect(page.locator('svg.safira-logo')).toHaveCount(0);
});

test('language is available on every screen', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Lessons' }).click();
  await expect(page.getByRole('button', { name: /^Theme: / })).toBeVisible();
  await expect(page.getByRole('button', { name: /^Language: / })).toBeVisible();

  await page.getByRole('button', { name: 'Back to projects' }).click();
  await page.getByRole('button', { name: 'Create project' }).click();
  await page.getByRole('button', { name: 'Go ahead' }).click();
  await page.getByRole('button', { name: /^Language: / }).click();
  await page.getByRole('button', { name: /^Idioma: / }).click();

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
    await expect(page.getByRole('menuitem', { name: 'Listas' })).toBeVisible();
    await expectNoViolations(page);
  });
});
