import Vue from 'vue';
import Vuex from 'vuex';

import { alert } from './alert.module';
import { account } from './account.module';
import { users } from './users.module';
import { product } from './product.module';
import { vending } from './vending.module';

Vue.use(Vuex);

export const store = new Vuex.Store({
    modules: {
        alert,
        account,
        users,
        product,
        vending
    }
});
