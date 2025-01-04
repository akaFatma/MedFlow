const { Builder, By, Key, until } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');

(async function loginTest() {
  // Initialize the Chrome driver
  let driver = await new Builder()
    .forBrowser('chrome')
    .setChromeOptions(new chrome.Options().headless()) // Run headless (without UI)
    .build();

  try {
    // Open the application (ensure it's running on localhost:4200)
    await driver.get('http://localhost:4200/login');  // Replace with your app's URL if different
    
    // Wait for the login form to be visible
    await driver.wait(until.elementLocated(By.css('form')), 10000); // Waiting for the form to load

    // Find the username and password input fields by their IDs
    let usernameField = await driver.findElement(By.id('username'));
    let passwordField = await driver.findElement(By.id('password'));

    // Clear any pre-filled values (if any)
    await usernameField.clear();
    await passwordField.clear();

    // Type in valid login credentials
    await usernameField.sendKeys('testuser');  // Use an actual test username
    await passwordField.sendKeys('testpassword');  // Use an actual test password

    // Find the submit button and click it
    let submitButton = await driver.findElement(By.css('button[type="submit"]'));
    await submitButton.click();

    // Wait for the result after login attempt (you can modify this based on the result page)
    await driver.wait(until.urlContains('/dashboard'), 5000);  // Wait for successful login redirection

    // Assert that the URL is correct after login (change '/dashboard' if your route is different)
    let currentUrl = await driver.getCurrentUrl();
    console.log('Current URL after login: ', currentUrl);

    // Example: Verify the user was successfully redirected to the dashboard
    if (currentUrl.includes('/dashboard')) {
      console.log('Login test passed: User redirected to dashboard');
    } else {
      console.error('Login test failed: User not redirected to dashboard');
    }
  } catch (error) {
    console.error('Test failed', error);
  } finally {
    // Quit the driver
    await driver.quit();
  }
})();
