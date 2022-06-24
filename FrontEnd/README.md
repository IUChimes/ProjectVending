Forked from: https://github.com/cornflourblue/vue-vuex-registration-login-example

# Notes

## PROS

* Has mocked JWT based auth
* Generally tidy structure, although non standard
* Separate `auth-header` function that includes necessary headers
* Set up basic router. (Redirect on auth failure)


## CONS

* Uses native `fetch` API instead of `axios` library.
* Everything is based on states
* Lots of repeating code
