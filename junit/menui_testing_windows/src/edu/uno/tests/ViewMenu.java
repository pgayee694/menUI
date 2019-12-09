package edu.uno.tests;

import java.util.regex.Pattern;
import java.util.concurrent.TimeUnit;
import org.junit.*;
import static org.junit.Assert.*;
import static org.hamcrest.CoreMatchers.*;
import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.Select;

public class ViewMenu {
  private WebDriver driver;
  private String baseUrl;
  private boolean acceptNextAlert = true;
  private StringBuffer verificationErrors = new StringBuffer();

  @Before
  public void setUp() throws Exception {
    driver = new FirefoxDriver();
    baseUrl = "https://www.katalon.com/";
    driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
  }

  @Test
  public void testViewMenu() throws Exception {
    driver.get("http://127.0.0.1:5000/");
    driver.findElement(By.linkText("Login")).click();
    driver.findElement(By.id("username")).click();
    driver.findElement(By.id("username")).clear();
    driver.findElement(By.id("username")).sendKeys("new");
    driver.findElement(By.id("password")).clear();
    driver.findElement(By.id("password")).sendKeys("new");
    driver.findElement(By.id("remember_me")).click();
    driver.findElement(By.id("submit1")).click();
    driver.findElement(By.id("searchimg")).click();
    // ERROR: Caught exception [ERROR: Unsupported command [addSelection | name=category | label=Delivery]]
    driver.findElement(By.xpath("(.//*[normalize-space(text()) and normalize-space(.)='Menu Search'])[2]/following::option[1]")).click();
    // ERROR: Caught exception [ERROR: Unsupported command [addSelection | name=cuisine | label=American]]
    driver.findElement(By.xpath("(.//*[normalize-space(text()) and normalize-space(.)='Menu Search'])[2]/following::option[16]")).click();
    // ERROR: Caught exception [ERROR: Unsupported command [addSelection | name=establishment | label=Fast Food]]
    driver.findElement(By.xpath("(.//*[normalize-space(text()) and normalize-space(.)='Menu Search'])[2]/following::option[94]")).click();
    driver.findElement(By.xpath("//input[@type='submit']")).click();
    driver.findElement(By.xpath("(.//*[normalize-space(text()) and normalize-space(.)='Add'])[4]/following::div[1]")).click();
    driver.findElement(By.xpath("//button[@onclick=\"window.location.href = 'https://www.zomato.com/omaha/five-guys-burgers-and-fries-papillion/menu?utm_source=api_basic_user&utm_medium=api&utm_campaign=v2.1&openSwipeBox=menu&showMinimal=1#tabtop'\"]")).click();
    driver.findElement(By.xpath("(.//*[normalize-space(text()) and normalize-space(.)='Phone number'])[1]/following::span[3]")).click();
    driver.findElement(By.xpath("(.//*[normalize-space(text()) and normalize-space(.)='Five Guys Burgers and Fries Menu'])[1]/following::div[5]")).click();
  }

  @After
  public void tearDown() throws Exception {
    driver.quit();
    String verificationErrorString = verificationErrors.toString();
    if (!"".equals(verificationErrorString)) {
      fail(verificationErrorString);
    }
  }

  private boolean isElementPresent(By by) {
    try {
      driver.findElement(by);
      return true;
    } catch (NoSuchElementException e) {
      return false;
    }
  }

  private boolean isAlertPresent() {
    try {
      driver.switchTo().alert();
      return true;
    } catch (NoAlertPresentException e) {
      return false;
    }
  }

  private String closeAlertAndGetItsText() {
    try {
      Alert alert = driver.switchTo().alert();
      String alertText = alert.getText();
      if (acceptNextAlert) {
        alert.accept();
      } else {
        alert.dismiss();
      }
      return alertText;
    } finally {
      acceptNextAlert = true;
    }
  }
}
