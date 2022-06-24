import { productService } from '../_services';

const state = {
    products: [{}]
};

const actions = {
    getProducts({ commit }) {
        productService.getProducts()
            .then(
                products => commit('getInfoSuccess', products),
                error => commit('getInfoSuccess', [])
            );
    },
};

const mutations = {
    getInfoSuccess(state, products) {
        state.products = products.products;
    },
};

export const product = {
    namespaced: true,
    state,
    actions,
    mutations
};
