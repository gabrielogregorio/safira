import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Page } from '@playwright/test';

const WCAG_AA_TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'];
const LAYOUT_WIDTHS = [320, 375, 768, 1280, 1440];

const expectNoViolations = async (page: Page): Promise<void> => {
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
  await page.getByLabel('Code editor').click();
  await page.keyboard.insertText(code);
};

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
  await page.locator('.toolbar-actions').getByRole('button', { name: 'Stop execution' }).click();

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
  await page.getByRole('button', { name: 'Open New project' }).click();
  await page.keyboard.press('Control+o');

  await expect(page.getByRole('dialog').getByRole('button', { name: 'lib.safira' })).toBeVisible();
});

test('debugs line by line with the variables panel', async ({ page }) => {
  await createProjectWithCode(page, 'x = 1\nmostre x');
  await page.keyboard.press('F6');
  await page.getByRole('button', { name: 'Next line' }).click();

  await expect(page.getByRole('cell', { name: 'x', exact: true })).toBeVisible();
});

test('colors the syntax of the code', async ({ page }) => {
  await createProjectWithCode(page, 'mostre "oi"');

  await expect(page.locator('.syntax-exibicao')).toHaveText('mostre');
  await expect(page.locator('.syntax-string')).toHaveText('"oi"');
});

test.describe('accessibility', () => {
  for (const theme of ['Simple', 'Dark', 'Light']) {
    test(`home and editor have no violations in the ${theme} theme`, async ({ page }) => {
      await page.goto('/');
      await page.getByLabel('Theme').selectOption({ label: theme });
      await expectNoViolations(page);

      await page.getByRole('button', { name: 'Create project' }).click();
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
    });
  }
});
