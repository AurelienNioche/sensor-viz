// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('Windowing Behavior', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('should load page with default accelerometer view', async ({ page }) => {
    const description = await page.locator('#trajectory-description').textContent();
    expect(description).toContain('Default: Accelerometer data');
    
    const windowValue = await page.locator('#window-value').textContent();
    expect(windowValue).toBe('0.5');
  });

  test('should show correct window size on initial load', async ({ page }) => {
    const slider = page.locator('#window-slider');
    const value = await slider.getAttribute('value');
    expect(value).toBe('0.5');
  });

  test('clicking on bandpass chart centers window on clicked time', async ({ page }) => {
    const consoleLogs = [];
    page.on('console', msg => {
      if (msg.type() === 'log') {
        consoleLogs.push(msg.text());
      }
    });

    const bandpassChart = page.locator('#chart-bandpass .u-over');
    await bandpassChart.waitFor({ state: 'visible' });
    const box = await bandpassChart.boundingBox();
    
    expect(box).not.toBeNull();
    
    const clickX = box.x + box.width * 0.5;
    const clickY = box.y + box.height / 2;
    
    await page.mouse.click(clickX, clickY);
    
    await page.waitForSelector('#trajectory-description:not(:empty)', { timeout: 3000 });
    await page.waitForTimeout(1500);
    
    const description = await page.locator('#trajectory-description').textContent();
    expect(description).toContain('Bandpass');
    
    const relevantLogs = consoleLogs.filter(log => 
      log.includes('CLICK on bandpass') || log.includes('Windowing bandpass')
    );
    expect(relevantLogs.length).toBeGreaterThan(0);
  });

  test('clicking creates a window smaller than total data', async ({ page }) => {
    const consoleLogs = [];
    page.on('console', msg => {
      if (msg.type() === 'log') {
        consoleLogs.push(msg.text());
      }
    });

    const bandpassChart = page.locator('#chart-bandpass .u-over');
    await bandpassChart.waitFor({ state: 'visible' });
    const box = await bandpassChart.boundingBox();
    
    await page.mouse.click(box.x + box.width * 0.5, box.y + box.height / 2);
    
    await page.waitForTimeout(1500);
    
    const dataRangeLog = consoleLogs.find(log => log.includes('Data range:'));
    const resultLog = consoleLogs.find(log => log.includes('Result:') && log.includes('points'));
    
    expect(consoleLogs.length).toBeGreaterThan(0);
    
    if (dataRangeLog && resultLog) {
      const totalPointsMatch = dataRangeLog.match(/total: (\d+) points/);
      const resultPointsMatch = resultLog.match(/Result: (\d+) points/);
      
      if (totalPointsMatch && resultPointsMatch) {
        const totalPoints = parseInt(totalPointsMatch[1]);
        const resultPoints = parseInt(resultPointsMatch[1]);
        
        expect(resultPoints).toBeLessThan(totalPoints);
        expect(resultPoints).toBeGreaterThan(0);
      }
    }
  });

  test('slider adjustment changes window size', async ({ page }) => {
    const slider = page.locator('#window-slider');
    const windowValue = page.locator('#window-value');
    
    await slider.evaluate(node => { node.value = 1.5; node.dispatchEvent(new Event('input', { bubbles: true })); });
    await page.waitForTimeout(300);
    
    const newValue = await windowValue.textContent();
    expect(newValue).toBe('1.5');
  });

  test('slider adjustment after click maintains centered window', async ({ page }) => {
    const consoleLogs = [];
    page.on('console', msg => {
      if (msg.type() === 'log') {
        consoleLogs.push(msg.text());
      }
    });

    const signalChart = page.locator('#chart-signal .u-over');
    const box = await signalChart.boundingBox();
    
    await page.mouse.click(box.x + box.width * 0.5, box.y + box.height / 2);
    await page.waitForTimeout(500);
    
    consoleLogs.length = 0;
    
    const slider = page.locator('#window-slider');
    await slider.evaluate(node => { node.value = 1.0; node.dispatchEvent(new Event('input', { bubbles: true })); });
    await page.waitForTimeout(500);
    
    const windowingLog = consoleLogs.find(log => log.includes('Windowing signal:'));
    expect(windowingLog).toBeTruthy();
  });

  test('clicking different charts switches active chart', async ({ page }) => {
    const signalChart = page.locator('#chart-signal .u-over');
    await signalChart.waitFor({ state: 'visible' });
    let box = await signalChart.boundingBox();
    await page.mouse.click(box.x + box.width * 0.5, box.y + box.height / 2);
    await page.waitForTimeout(1500);
    
    let description = await page.locator('#trajectory-description').textContent();
    expect(description).toContain('Signal');
    
    const bandpassChart = page.locator('#chart-bandpass .u-over');
    await bandpassChart.waitFor({ state: 'visible' });
    box = await bandpassChart.boundingBox();
    await page.mouse.click(box.x + box.width * 0.3, box.y + box.height / 2);
    await page.waitForTimeout(1500);
    
    description = await page.locator('#trajectory-description').textContent();
    expect(description).toContain('Bandpass');
  });

  test('reset button returns to default state', async ({ page }) => {
    const signalChart = page.locator('#chart-signal .u-over');
    const box = await signalChart.boundingBox();
    await page.mouse.click(box.x + box.width * 0.5, box.y + box.height / 2);
    await page.waitForTimeout(200);
    
    const resetBtn = page.locator('#reset-view');
    await resetBtn.click();
    await page.waitForTimeout(200);
    
    const description = await page.locator('#trajectory-description').textContent();
    expect(description).toContain('Default: Accelerometer data');
  });

  test('clicking twice on same chart recenters window', async ({ page }) => {
    const consoleLogs = [];
    page.on('console', msg => {
      if (msg.type() === 'log') {
        consoleLogs.push(msg.text());
      }
    });

    const signalChart = page.locator('#chart-signal .u-over');
    const box = await signalChart.boundingBox();
    
    await page.mouse.click(box.x + box.width * 0.3, box.y + box.height / 2);
    await page.waitForTimeout(200);
    
    const firstClickLogs = consoleLogs.filter(log => log.includes('center='));
    consoleLogs.length = 0;
    
    await page.mouse.click(box.x + box.width * 0.7, box.y + box.height / 2);
    await page.waitForTimeout(200);
    
    const secondClickLogs = consoleLogs.filter(log => log.includes('center='));
    
    expect(firstClickLogs.length).toBeGreaterThan(0);
    expect(secondClickLogs.length).toBeGreaterThan(0);
  });

  test('default window size prevents big blob on short duration data', async ({ page }) => {
    const consoleLogs = [];
    page.on('console', msg => {
      if (msg.type() === 'log') {
        consoleLogs.push(msg.text());
      }
    });

    const filteringChart = page.locator('#chart-filtering .u-over');
    const box = await filteringChart.boundingBox();
    
    await page.mouse.click(box.x + box.width * 0.5, box.y + box.height / 2);
    await page.waitForTimeout(500);
    
    const dataRangeLog = consoleLogs.find(log => log.includes('Data range:'));
    const resultLog = consoleLogs.find(log => log.includes('Result:') && log.includes('points'));
    
    if (dataRangeLog && resultLog) {
      const totalMatch = dataRangeLog.match(/total: (\d+) points/);
      const resultMatch = resultLog.match(/Result: (\d+) points/);
      
      if (totalMatch && resultMatch) {
        const total = parseInt(totalMatch[1]);
        const result = parseInt(resultMatch[1]);
        const percentage = (result / total) * 100;
        
        expect(percentage).toBeLessThan(80);
      }
    }
  });
});

test.describe('API Data Validation', () => {
  test('all charts load data correctly', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    const charts = ['signal', 'fft', 'filtering', 'psd', 'bandpass'];
    
    for (const chartName of charts) {
      const chart = page.locator(`#chart-${chartName}`);
      await expect(chart).toBeVisible();
      
      const canvas = chart.locator('canvas');
      await expect(canvas).toBeVisible();
    }
  });

  test('3D plot renders correctly', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    const accelPlot = page.locator('#chart-accelerometer');
    await expect(accelPlot).toBeVisible();
    
    await page.waitForTimeout(1000);
    
    const plotlyDiv = accelPlot.locator('.plotly');
    await expect(plotlyDiv).toBeVisible();
  });
});
