import Vue from 'vue';
import VeeValidate from 'vee-validate';

import { store } from './_store';
import { router } from './_helpers';
import App from './app/App';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

Vue.use(VeeValidate);
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

// setup fake backend
import { configureFakeBackend } from './_helpers';
configureFakeBackend();

new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
});