# E2E Testing with Playwright

## Overview

This directory contains end-to-end (E2E) tests using **Playwright** - the modern, industry-standard browser automation framework recommended by Microsoft, Google, and used by thousands of companies.

## Why Playwright?

✅ **Industry Standard**: Used by Microsoft, Google, Amazon, Netflix
✅ **Modern**: Auto-waiting, retry logic, parallel execution
✅ **Fast**: Headless browsers, smart test isolation
✅ **Comprehensive**: Real browser testing (not just mocks)
✅ **Developer Experience**: Great debugging tools, trace viewer, UI mode

## Running Tests

### Basic Commands

```bash
# Run all tests
npm test

# Run in UI mode (interactive)
npm run test:ui

# Run in headed mode (see browser)
npm run test:headed

# Debug mode (step through tests)
npm run test:debug

# View last test report
npm run test:report
```

### Advanced Usage

```bash
# Run specific test file
npx playwright test windowing.spec.js

# Run specific test
npx playwright test -g "clicking on bandpass"

# Run with specific browser
npx playwright test --project=chromium

# Generate trace for failed tests
npx playwright test --trace on

# Show trace
npx playwright show-trace test-results/path/to/trace.zip
```

## Test Structure

```
e2e/
├── README.md                 # This file
└── windowing.spec.js         # Windowing behavior tests (12 tests)
```

### Test Categories

**Windowing Behavior (10 tests)**
- Initial load state
- Click-to-center functionality
- Slider adjustments
- Chart switching
- Reset functionality
- Complex interaction flows

**API/Data Validation (2 tests)**
- Chart loading
- 3D plot rendering

## Current Status

**Pass Rate**: 75% (9/12 tests passing)

**Passing Tests**:
- ✅ Default accelerometer view loads
- ✅ Correct window size on load
- ✅ Slider changes window size
- ✅ Slider maintains centered window after click
- ✅ Reset button works
- ✅ Multiple clicks on same chart
- ✅ Window size prevents big blob
- ✅ All charts load data
- ✅ 3D plot renders

**Flaky/Failing Tests** (timing issues, needs refinement):
- ⚠️ Clicking bandpass centers window
- ⚠️ Window smaller than total data
- ⚠️ Switching between different charts

## Writing Tests

### Basic Test Structure

```javascript
test('description of what is being tested', async ({ page }) => {
  // Navigate
  await page.goto('/');
  
  // Interact
  await page.click('#some-button');
  
  // Assert
  await expect(page.locator('#result')).toContainText('expected');
});
```

### Best Practices

1. **Wait for elements**: `await element.waitFor({ state: 'visible' })`
2. **Use locators**: `page.locator('#id')` not CSS selectors
3. **Auto-waiting**: Playwright waits for elements automatically
4. **Console logging**: Capture `console.log` for debugging
5. **Screenshots**: Auto-captured on failure
6. **Timeouts**: Use sparingly, prefer waitFor conditions

### Console Log Testing

```javascript
const consoleLogs = [];
page.on('console', msg => {
  if (msg.type() === 'log') {
    consoleLogs.push(msg.text());
  }
});

// Later...
const relevantLog = consoleLogs.find(log => log.includes('CLICK'));
expect(relevantLog).toBeDefined();
```

### Slider Interaction

```javascript
// For range inputs, use evaluate to trigger properly
await slider.evaluate(node => {
  node.value = 1.5;
  node.dispatchEvent(new Event('input', { bubbles: true }));
});
```

## Debugging Failed Tests

### 1. View Screenshots

Failed tests auto-generate screenshots:
```bash
open test-results/*/test-failed-1.png
```

### 2. View Trace

Traces show everything that happened:
```bash
npx playwright show-trace test-results/path/to/trace.zip
```

### 3. Run in UI Mode

Interactive debugging:
```bash
npm run test:ui
```

### 4. Run Headed

See the browser:
```bash
npm run test:headed
```

### 5. Debug Mode

Step through line-by-line:
```bash
npm run test:debug
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install dependencies
        run: |
          npm install
          npx playwright install --with-deps
      - name: Run tests
        run: npm test
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

## Improving Test Reliability

### Common Issues

1. **Timing**: Use `waitFor` instead of `waitForTimeout`
2. **Animations**: Wait for animations to complete
3. **Network**: Use `waitForLoadState('networkidle')`
4. **Race conditions**: Use proper waitFor conditions

### Example Fixes

```javascript
// Bad
await page.click('#button');
await page.waitForTimeout(1000);

// Good
await page.click('#button');
await page.waitForSelector('#result:not(:empty)');

// Better
await page.click('#button');
await expect(page.locator('#result')).toBeVisible();
```

## Resources

- [Playwright Documentation](https://playwright.dev/)
- [Best Practices](https://playwright.dev/docs/best-practices)
- [Debugging Guide](https://playwright.dev/docs/debug)
- [CI/CD Guide](https://playwright.dev/docs/ci)

## Standard Practices in Web Development

### Testing Pyramid

Modern web apps should have:

1. **Unit Tests** (70%): Fast, isolated (Jest/Vitest)
   - Pure functions
   - Business logic
   - Utils

2. **Integration Tests** (20%): API, components (Testing Library)
   - API endpoints ✅ (We have this in `tests/test_api.py`)
   - Component interactions

3. **E2E Tests** (10%): Full user flows (Playwright/Cypress)
   - Critical paths ✅ (This directory)
   - User journeys
   - Cross-browser

### This Project

✅ **Backend Unit Tests**: pytest (48 tests, 100% coverage)
✅ **Backend Integration Tests**: FastAPI TestClient (15 tests)
✅ **Frontend E2E Tests**: Playwright (12 tests, 75% pass)
⚠️ **Frontend Unit Tests**: Missing (would add Jest/Vitest for charts.js)

### Industry Tools

- **Playwright** (✅ We use): Microsoft, modern, fast
- **Cypress**: Older alternative, still popular
- **Selenium**: Legacy, slow, avoid for new projects
- **Puppeteer**: Google's tool, less features than Playwright

## Next Steps

1. **Fix flaky tests**: Replace timeouts with proper waits
2. **Add more E2E tests**: Edge cases, error scenarios
3. **Add JS unit tests**: Test chart initialization functions
4. **Visual regression**: Add Percy/Chromatic for UI changes
5. **Performance tests**: Lighthouse CI for metrics
