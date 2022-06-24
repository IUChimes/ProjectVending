Forked from: https://github.com/cornflourblue/vue-vuex-registration-login-example

# Notes

Working features:
* Login
* Logout (Redirect only, does not delete JWT token)
* User Information display

Semi Working:
* Product Table with `buy` action. Issues with `fetch` API due to wrong datatype being expected at the backend.

Missing features:
* User Create/Modify/Delete
* Product View Private/Modify/Delete
* Deposit
* Reset
* Seller View

## PROS

* Has mocked JWT based auth
* Generally tidy structure, although non standard
* Separate `auth-header` function that includes necessary headers
* Set up basic router. (Redirect on auth failure)


## CONS

* Uses native `fetch` API instead of `axios` library.
* Everything is based on states
* Poor proxy setup that requires `/api` prefix.
* Lots of duplicate code
Such as:
```
    loginFailure(state) {
        state.status = {};
        state.user = null;
    },
    logout(state) {
        state.status = {};
        state.user = null;
    },
```
