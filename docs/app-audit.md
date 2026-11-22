# App Audit: Sauce Labs My Demo App (Android)

## App details

| Field              | Value                                                                         |
| ------------------ | ----------------------------------------------------------------------------- |
| Source             | Official saucelabs GitHub releases (github.com/saucelabs/my-demo-app-android) |
| Package            | `com.saucelabs.mydemoapp.android`                                             |
| Version            | 2.3.0 (versionCode 27)                                                        |
| Min SDK            | 21                                                                            |
| Target SDK         | 31 (Android 12); runs on API 35 emulator                                      |
| Launcher activity  | `.view.activities.SplashActivity`                                             |
| App-ready activity | `.view.activities.MainActivity` (used as `appWaitActivity`)                   |
| Verified with      | `apkanalyzer manifest ...`, `adb shell cmd package resolve-activity --brief`  |

## Grading scale

| Grade | Meaning                                                          |
| ----- | ---------------------------------------------------------------- |
| A     | Accessibility id (`content-desc`)                                |
| B     | Unique resource-id                                               |
| C     | Text match via UiAutomator, or a find scoped to a parent element |
| D     | XPath only (positional or attribute-heavy)                       |

Rule: grade the best locator available, not the one Inspector suggests.

## Locator audit

| Screen           | Element                         | Best locator                                                                                                     | Strategy                             | Grade |
| ---------------- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------ | ----- |
| Catalogue        | Screen title                    | `title`                                                                                                          | ACCESSIBILITY_ID                     | A     |
| Catalogue        | Product name (specific product) | `new UiSelector().description("Product Title").text("Sauce Labs Backpack")`                                      | ANDROID_UIAUTOMATOR                  | C     |
| Catalogue        | Product price (all visible)     | `Product Price` (`find_elements`, same order as titles)                                                          | ACCESSIBILITY_ID                     | A     |
| Catalogue        | Sort button                     | `Shows current sorting order and displays available sorting options`                                             | ACCESSIBILITY_ID                     | A     |
| Catalogue        | Cart icon                       | `Displays number of items in your cart`                                                                          | ACCESSIBILITY_ID                     | A     |
| Product details  | Name                            | `com.saucelabs.mydemoapp.android:id/productTV`                                                                   | ID                                   | B     |
| Product details  | Price                           | `com.saucelabs.mydemoapp.android:id/priceTV`                                                                     | ID                                   | B     |
| Product details  | Quantity                        | `com.saucelabs.mydemoapp.android:id/noTV`                                                                        | ID                                   | B     |
| Product details  | Increase quantity (+)           | `Increase item quantity`                                                                                         | ACCESSIBILITY_ID                     | A     |
| Product details  | Decrease quantity (-)           | `Decrease item quantity`                                                                                         | ACCESSIBILITY_ID                     | A     |
| Product details  | Add to cart                     | `Tap to add product to cart`                                                                                     | ACCESSIBILITY_ID                     | A     |
| Cart             | Item rows                       | List: `Displays list of selected products`, then its `android.view.ViewGroup` children (`find_elements`, scoped) | ACCESSIBILITY_ID + scoped CLASS_NAME | C     |
| Cart             | Quantity (per row)              | `com.saucelabs.mydemoapp.android:id/noTV`, found inside a row element                                            | ID (row-scoped)                      | B     |
| Cart             | Total                           | `com.saucelabs.mydemoapp.android:id/totalPriceTV`                                                                | ID                                   | B     |
| Cart             | Proceed to checkout             | `Confirms products for checkout`                                                                                 | ACCESSIBILITY_ID                     | A     |
| Login (via menu) | Username                        | `com.saucelabs.mydemoapp.android:id/nameET`                                                                      | ID                                   | B     |
| Login (via menu) | Password                        | `com.saucelabs.mydemoapp.android:id/passwordET`                                                                  | ID                                   | B     |
| Login (via menu) | Login button                    | `Tap to login with given credentials`                                                                            | ACCESSIBILITY_ID                     | A     |
| Login (via menu) | Error message                   | Deferred: audit on Login day                                                                                     | -                                    | -     |
| Checkout         | Address field                   | Deferred: audit on Checkout day                                                                                  | -                                    | -     |
| Checkout         | Continue / To payment           | Deferred: audit on Checkout day                                                                                  | -                                    | -     |
| Checkout         | Card field                      | Deferred: audit on Checkout day                                                                                  | -                                    | -     |
| Checkout         | Place order                     | Deferred: audit on Checkout day                                                                                  | -                                    | -     |
| Checkout         | Confirmation text               | Deferred: audit on Checkout day                                                                                  | -                                    | -     |

## Notes on the non-A/B elements

- **Product name:** all product titles share `content-desc="Product Title"`, so a specific product is selected by text through UiAutomator. Reading all names uses `find_elements(ACCESSIBILITY_ID, "Product Title")`, which is grade A.
- **Cart rows:** no per-row id exists. Rows are found as children of the list element, and every value inside a row (quantity, price) is found with a row-scoped `find_element`. No positional XPath (`ViewGroup[1]`).
- **`noTV`** is reused on Product details and Cart. It is unique on Product details; in the Cart it is only used inside a row.

## Grade counts (18 audited)

| A   | B   | C   | D   |
| --- | --- | --- | --- |
| 9   | 7   | 2   | 0   |

A + B = 89%

## Decision: GO

89% of audited elements have accessibility ids or unique resource-ids. The remaining two are handled by a UiAutomator text match and row-scoped finds, with no positional XPath. The login error message and checkout elements will be audited on the days their screen objects are built.

## Manifest findings (`docs/manifest.xml`)

| Finding                                                       | Impact on the test plan                                                     |
| ------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `MainActivity` is portrait-locked (`screenOrientation="1"`)   | No rotation tests on this app; rotation moves to the WebdriverIO demo app   |
| No deep-link intent filters (`<data android:scheme>`)         | No deep-link tests on this app; deep links move to the WebdriverIO demo app |
| `CAMERA`, `ACCESS_FINE_LOCATION`, `USE_BIOMETRIC` permissions | Material for permission-dialog and biometric tests in Week 2                |
| Splash activity hands over to `MainActivity`                  | `appWaitActivity = *.MainActivity` set, so session start is not flaky       |
| `android:debuggable="true"`                                   | Test build, suitable for automation                                         |
| Bundled TestFairy feedback SDK (`ProvideFeedbackActivity`)    | Watch for unexpected feedback pop-ups during runs                           |
| Target SDK 31 on an API 35 emulator                           | Runs in compatibility mode; minor risk, not a blocker                       |

## Open items

- [ ] Confirm cart-row class under "Displays list of selected products" (assumed `android.view.ViewGroup`), on Cart day
- [ ] Audit login error message, on Login day
- [ ] Audit checkout elements, on Checkout day
