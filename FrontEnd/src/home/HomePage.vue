<template>
  <div>
    <div>
      Username: {{ user.username }}
      <br />
      Deposit: {{ user.deposit }}
      <br />
      Role: {{ user.role }}
    </div>

    <b-table
      head-variant="dark"
      hover
      :items="products"
      :fields="fields"
      primary-key="rowID"
    >
      <template #cell(actions)="data">
        <b-button
          variant="outline-success"
          v-b-modal.modal-1
          @click="beforeOpenPurchaseModel(data)"
          >Buy</b-button
        >
      </template>
    </b-table>
    <p>
      <router-link to="/login">Logout</router-link>
    </p>
    <b-modal id="modal-1" title="BootstrapVue" @ok="purchase">
      <b-form-input
        v-model="amount"
        type="number"
        :state="amount > 0"
      ></b-form-input>
    </b-modal>
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";

export default {
  data() {
    return {
      amount: 0,
      product: {},
      fields: [
        {
          key: "productName",
          label: "Person age",
          sortable: true,
        },
        {
          key: "cost",
          label: "Cost",
          sortable: false,
        },
        {
          key: "amountAvailable",
          label: "Available",
          sortable: true,
          _showDetails: true,
        },
        {
          key: "sellerUsername",
          label: "Seller",
          sortable: true,
        },
        { key: "actions" },
      ],
    };
  },
  computed: {
    user() {
      return this.$store.state.users.current_user;
    },
    products() {
      return this.$store.state.product.products;
    },
  },
  created() {
    this.getUserInfo();
    this.getProducts();
  },
  methods: {
    ...mapActions("users", {
      getUserInfo: "getInfo",
    }),
    ...mapActions("product", {
      getProducts: "getProducts",
    }),
    ...mapActions("vending", {
      buy: "buy",
    }),
    beforeOpenPurchaseModel(data) {
      this.product = data;
      this.$store.state.vending.productID = data.item.rowID;
    },
    purchase() {
      this.$store.state.vending.amount = this.amount;
      this.buy(this.product.rowID, this.amount);
      this.amount = 0;
    },
  },
};
</script>
