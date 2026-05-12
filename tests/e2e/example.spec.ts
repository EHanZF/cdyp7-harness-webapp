import { test, expect } from '@playwright/test';

test('homepage returns 200', async ({ request }) => {
  const resp = await request.get('/');
  expect(resp.status()).toBe(200);
});
