(async (page) => {
  const base = 'http://127.0.0.1:3002';
  const records = [];
  const pageErrors = [];
  const badResponses = [];
  const hardConsole = [];
  let currentStep = 'bootstrap';

  const local = (url) => url.includes('127.0.0.1:3002') || url.includes('127.0.0.1:7860');
  const hardText = /Application error|Unexpected Application Error|Cannot read properties|TypeError|ReferenceError|Internal Server Error|Request failed/i;

  page.on('pageerror', (error) => pageErrors.push({ step: currentStep, message: error.message }));
  page.on('response', (response) => {
    if (local(response.url()) && response.status() >= 400) {
      badResponses.push({ step: currentStep, status: response.status(), url: response.url() });
    }
  });
  page.on('console', (msg) => {
    const text = msg.text();
    if (msg.type() === 'error' && hardText.test(text)) {
      hardConsole.push({ step: currentStep, text: text.slice(0, 500) });
    }
  });

  const settle = async () => {
    await page.waitForLoadState('domcontentloaded', { timeout: 10000 }).catch(() => {});
    await page.waitForLoadState('networkidle', { timeout: 4000 }).catch(() => {});
    await page.waitForTimeout(700);
  };

  const inspect = async (label, action, before) => {
    await settle();
    const state = await page.evaluate((pattern) => {
      const text = document.body?.innerText || '';
      return {
        href: location.href,
        route404: location.pathname.endsWith('/404') || /页面不存在|Page Not Found|404 Not Found/i.test(text),
        runtimeError: new RegExp(pattern, 'i').test(text),
        text: text.replace(/\s+/g, ' ').slice(0, 280),
      };
    }, hardText.source);
    records.push({
      label,
      action,
      ...state,
      pageErrors: pageErrors.slice(before.pageErrors),
      badResponses: badResponses.slice(before.badResponses),
      hardConsole: hardConsole.slice(before.hardConsole),
    });
  };

  const before = () => ({
    pageErrors: pageErrors.length,
    badResponses: badResponses.length,
    hardConsole: hardConsole.length,
  });

  const run = async (label, path, action) => {
    currentStep = label;
    await page.goto(`${base}${path}`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await settle();
    const mark = before();
    try {
      await action();
    } catch (error) {
      records.push({ label, action: 'action failed', href: page.url(), clickError: error.message.slice(0, 500) });
    }
    await inspect(label, action.name || 'anonymous action', mark);
    await page.keyboard.press('Escape').catch(() => {});
    await page.waitForTimeout(250);
  };

  const clickText = (text, exact = true) => async function clickByText() {
    await page.getByText(text, { exact }).first().click({ timeout: 8000 });
  };

  const optionalClickText = (text, exact = true) => async function optionalClickByText() {
    const locator = page.getByText(text, { exact }).first();
    const count = await locator.count().catch(() => 0);
    if (!count) return;
    const visible = await locator.isVisible().catch(() => false);
    if (!visible) return;
    await locator.click({ timeout: 8000 });
  };

  const clickRole = (role, name) => async function clickByRole() {
    await page.getByRole(role, { name }).first().click({ timeout: 8000 });
  };

  await run('platform.build.newApp', '/build/apps', clickText('新建应用'));
  await run('platform.filelib.create', '/filelib', clickText('创建'));
  await run('platform.dataset.create', '/dataset', clickText('创建数据集'));
  await run('platform.model.add', '/model/management', clickText('添加模型'));
  await run('platform.evaluation.create', '/evaluation', clickText('创建'));
  await run('platform.label.create', '/label', clickText('创建标注任务'));
  await run('platform.dashboard.fullscreen', '/dashboard', clickText('全屏'));
  await run('platform.dashboard.share', '/dashboard', clickText('分享'));
  await run('workspace.knowledge.dialog', '/workspace/apps', clickText('个人知识库'));
  await run('workspace.linsight.share', '/workspace/linsight', optionalClickText('分享'));
  await run('workspace.chat.fillInput', '/workspace/c/new', async function fillChatInput() {
    const box = page.getByRole('textbox').first();
    if (await box.isDisabled().catch(() => true)) return;
    await box.fill('测试一知工作台输入框');
  });
  await run('workspace.apps.categoryCommon', '/workspace/apps', clickRole('button', '常用'));
  await run('workspace.apps.categoryUnclassified', '/workspace/apps', clickRole('button', '未分类'));

  const summaryRecords = records.map((record) => ({
    label: record.label,
    href: record.href,
    route404: record.route404,
    runtimeError: record.runtimeError,
    pageErrorCount: record.pageErrors?.length || 0,
    badResponseCount: record.badResponses?.length || 0,
    hardConsoleCount: record.hardConsole?.length || 0,
    clickError: record.clickError || '',
    sample: record.text || '',
    badResponses: record.badResponses || [],
    pageErrors: record.pageErrors || [],
    hardConsole: record.hardConsole || [],
  }));
  return {
    visitedCount: summaryRecords.length,
    visited: summaryRecords.map(({ label, href }) => ({ label, href })),
    failures: summaryRecords.filter((record) => (
      record.route404 ||
      record.runtimeError ||
      record.pageErrorCount ||
      record.badResponseCount ||
      record.hardConsoleCount ||
      record.clickError
    )),
  };
})
