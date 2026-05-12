# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: example.spec.ts >> homepage returns 200
- Location: tests\e2e\example.spec.ts:3:5

# Error details

```
TypeError: apiRequestContext.get: Invalid URL
```

# Test source

```ts
  1 | import { test, expect } from '@playwright/test';
  2 | 
  3 | test('homepage returns 200', async ({ request }) => {
> 4 |   const resp = await request.get('/');
    |                              ^ TypeError: apiRequestContext.get: Invalid URL
  5 |   expect(resp.status()).toBe(200);
  6 | });
  7 | 
```