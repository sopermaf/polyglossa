<template>
  <v-app>
    <!-- Header -->
    <PolyToolbar
      :isSPAToolbar="false"
    />

    <!-- Page Content -->
    <v-content>
      <v-container>
        <v-layout justify-center wrap class="mx-auto">

            <!-- Order Overview -->
            <v-flex ma-5 lg6 s12 xs12>
                <v-card outlined>
                    <v-card-title>
                        Order Details
                    </v-card-title>
                    <v-card-text>
                        <v-simple-table>
                            <tbody>
                                <tr v-for="detail in order" :key="detail.title">
                                    <td><b>{{ detail.title.toUpperCase() }}</b></td>
                                    <td>{{ detail.value }}</td>
                                </tr>
                            </tbody>
                        </v-simple-table>
                    </v-card-text>
                </v-card>
            </v-flex>

            <div class="break" />

            <!-- Orders with Payment -->
            <template v-if="button">
              <v-flex v-if="button" mt-2 lg3 s4 xs12 text-center>
                  <v-form :action="button.url" method="post">
                      <input type="hidden" name="cmd" value="_s-xclick" />
                      <input type="hidden" name="encrypted" :value="button.encrypted_inputs"/>
                      <input
                          type="image"
                          :src="require('./assets/paypal-checkout-logo-large.png')"
                          
                          border="0"
                          name="submit"
                          alt="Check out with PayPal"
                      />
                  </v-form>
              </v-flex>
              <v-flex mt-2 lg3 s4 xs12 text-center>
                  <v-btn @click="cancelOrder">
                      Cancel
                  </v-btn>
              </v-flex>
            </template>

            <!-- Free Orders -->
            <v-flex v-else mt-2 lg3 s4 xs12 text-center>
              <v-btn @click="returnHome">
                    Return to Home Page
              </v-btn>
            </v-flex>

        </v-layout>
      </v-container>
    </v-content>

    <!-- Footer -->
    <PolyFooter />
  </v-app>
</template>

<script>
import axios from "axios";

import PolyToolbar from "./components/PolyToolbar.vue";
import PolyFooter from "./components/PolyFooter.vue";

export default {
  name: "Payment",
  components: {
    PolyToolbar,
    PolyFooter,
  },
  data: () => ({
    video_id: "",
    title: "",
    order: null,
    button: null
  }),
  mounted() {
    var paymentInfo = JSON.parse(document.body.getAttribute('data'));

    this.button = paymentInfo.button;
    this.order = paymentInfo.order;
  },
  methods: {
    returnHome() {
      window.location.href = '/';
    },
    cancelOrder() {
        axios.post('/payments/cancel/');
        this.returnHome();
    },
  },
};
</script>

<style lang="scss">  
tbody {
    tr:hover {
      background-color: transparent !important;
    }
}

.break {
  flex-basis: 100%;
  height: 0;
}
</style>