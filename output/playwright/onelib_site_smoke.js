(async (page) => {
  const base = 'http://127.0.0.1:3002';
  const results = [];
  const consoleEntries = [];
  const pageErrors = [];
  const failedRequests = [];
  const badResponses = [];
  let currentStep = 'bootstrap';

  const isLocalUrl = (url) => url.includes('127.0.0.1:3002') || url.includes('127.0.0.1:7860');

  page.on('console', (msg) => {
    if (['error', 'warning'].includes(msg.type())) {
      consoleEntries.push({ step: currentStep, type: msg.type(), text: msg.text().slice(0, 600) });
    }
  });
  page.on('pageerror', (error) => {
    pageErrors.push({ step: currentStep, message: error.message.slice(0, 600) });
  });
  page.on('requestfailed', (request) => {
    const url = request.url();
    if (isLocalUrl(url)) {
      failedRequests.push({
        step: currentStep,
        method: request.method(),
        url,
        error: request.failure()?.errorText || '',
      });
    }
  });
  page.on('response', (response) => {
    const url = response.url();
    if (isLocalUrl(url) && response.status() >= 400) {
      badResponses.push({ step: currentStep, status: response.status(), url });
    }
  });

  const settle = async () => {
    await page.waitForLoadState('domcontentloaded', { timeout: 10000 }).catch(() => {});
    await page.waitForLoadState('networkidle', { timeout: 5000 }).catch(() => {});
    await page.waitForTimeout(900);
  };

  const inspect = async (label, action) => {
    currentStep = label;
    await settle();
    const state = await page.evaluate(() => {
      const text = document.body?.innerText || '';
      const route404 = location.pathname.endsWith('/404') || /页面不存在|Page Not Found|404 Not Found/i.test(text);
      const runtimeError = /Application error|Unexpected Application Error|Cannot read properties|TypeError|ReferenceError|Internal Server Error|Request failed/i.test(text);
      return {
        href: location.href,
        title: document.title,
        route404,
        runtimeError,
        text: text.replace(/\s+/g, ' ').slice(0, 500),
      };
    });
    results.push({ label, action, ...state });
  };

  const visit = async (label, path) => {
    currentStep = label;
    await page.goto(`${base}${path}`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await inspect(label, `goto ${path}`);
  };

  const clickText = async (label, text, exact = true) => {
    currentStep = label;
    const locator = page.getByText(text, { exact }).first();
    const count = await locator.count().catch(() => 0);
    if (!count) {
      results.push({ label, action: `click text ${text}`, skipped: true, reason: 'text not found', href: page.url() });
      return;
    }
    const visible = await locator.isVisible().catch(() => false);
    if (!visible) {
      results.push({ label, action: `click text ${text}`, skipped: true, reason: 'text not visible', href: page.url() });
      return;
    }
    await locator.click({ timeout: 8000 }).catch((error) => {
      results.push({ label, action: `click text ${text}`, clickError: error.message.slice(0, 500), href: page.url() });
    });
    await inspect(label, `click text ${text}`);
  };

  const optionalClickText = async (label, text, exact = true) => {
    currentStep = label;
    const locator = page.getByText(text, { exact }).first();
    const count = await locator.count().catch(() => 0);
    if (!count) {
      results.push({ label, action: `optional click text ${text}`, skipped: true, reason: 'text not found', href: page.url() });
      return;
    }
    const visible = await locator.isVisible().catch(() => false);
    if (!visible) {
      results.push({ label, action: `optional click text ${text}`, skipped: true, reason: 'text not visible', href: page.url() });
      return;
    }
    await locator.click({ timeout: 8000 }).catch((error) => {
      results.push({ label, action: `optional click text ${text}`, clickError: error.message.slice(0, 500), href: page.url() });
    });
    await inspect(label, `optional click text ${text}`);
  };

  const clickRole = async (label, role, name) => {
    currentStep = label;
    const locator = page.getByRole(role, { name }).first();
    const count = await locator.count().catch(() => 0);
    if (!count) {
      results.push({ label, action: `click role ${role}:${name}`, skipped: true, reason: 'role not found', href: page.url() });
      return;
    }
    await locator.click({ timeout: 8000 }).catch((error) => {
      results.push({ label, action: `click role ${role}:${name}`, clickError: error.message.slice(0, 500), href: page.url() });
    });
    await inspect(label, `click role ${role}:${name}`);
  };

  const platformRoutes = [
    ['platform.dashboard', '/dashboard'],
    ['platform.build.apps', '/build/apps'],
    ['platform.build.tools', '/build/tools'],
    ['platform.build.client', '/build/client'],
    ['platform.filelib', '/filelib'],
    ['platform.dataset', '/dataset'],
    ['platform.model.management', '/model/management'],
    ['platform.model.finetune', '/model/finetune'],
    ['platform.evaluation', '/evaluation'],
    ['platform.label', '/label'],
    ['platform.log', '/log'],
    ['platform.sys', '/sys'],
  ];

  for (const [label, path] of platformRoutes) {
    await visit(label, path);
  }

  await visit('platform.filelib.tabs', '/filelib');
  await clickText('platform.filelib.tab.document', '文档知识库');
  await clickText('platform.filelib.tab.qa', 'QA知识库');

  await visit('platform.log.tabs', '/log');
  await clickText('platform.log.tab.app', '应用使用');
  await clickText('platform.log.tab.system', '系统操作');

  await visit('platform.sys.tabs', '/sys');
  for (const text of ['用户管理', '用户组管理', '角色管理', '系统配置', '主题配色']) {
    await clickText(`platform.sys.tab.${text}`, text);
  }

  await visit('platform.model.tabs', '/model/management');
  await clickText('platform.model.link.management', '模型管理');
  await clickText('platform.model.link.finetune', '模型微调');

  await visit('workspace.chat.new', '/workspace/c/new');
  await clickRole('workspace.chat.open.apps', 'button', /应用中心|App Center/i);
  await clickRole('workspace.apps.new.chat', 'button', /开始新对话|开启新对话|New Chat/i);

  await visit('workspace.apps', '/workspace/apps');
  await clickRole('workspace.apps.start.new.chat', 'button', /开始新对话|开启新对话|New Chat/i);

  await visit('workspace.linsight', '/workspace/linsight');
  for (const text of ['任务描述', '工具配置', '执行结果']) {
    await optionalClickText(`workspace.linsight.${text}`, text);
  }

  const failures = results.filter((item) => item.route404 || item.runtimeError || item.clickError);
  return {
    visitedCount: results.length,
    visited: results.map(({ label, action, href, skipped, reason }) => ({ label, action, href, skipped: !!skipped, reason: reason || '' })),
    failures,
    pageErrors,
    failedRequests,
    badResponses,
    consoleSummary: consoleEntries.reduce((acc, item) => {
      const key = `${item.step}:${item.type}:${item.text.split('\n')[0].slice(0, 90)}`;
      acc[key] = (acc[key] || 0) + 1;
      return acc;
    }, {}),
  };
})
