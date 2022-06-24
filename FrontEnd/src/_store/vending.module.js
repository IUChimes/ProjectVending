import { vendingService } from "../_services";

const state = {
    productID: 0,
    amount: 0,
};

const actions = {
  buy({state}) {
    vendingService.buy(state.productID, state.amount);
    /*.then(
                products => commit('getInfoSuccess', products),
                error => commit('getInfoSuccess', [])
            );*/
  },
};

/*const mutations = {
    getInfoSuccess(state, products) {
        state.products = products.products;
    },
};*/

export const vending = {
  namespaced: true,
  state,
  actions,
  //mutations
};
