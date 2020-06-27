<template>
    <v-container>
        <v-layout justify-center wrap class="mx-auto">
            <v-flex ma-5 lg6 s12 xs12>
                <v-card outlined>
                    <v-card-title>
                        Order Review
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

            <v-flex mt-2 lg3 s4 xs12 text-center>
                <v-form :action="button.url" method="post">
                    <input type="hidden" name="cmd" value="_s-xclick" />
                    <input type="hidden" name="encrypted" :value="button.encrypted_inputs"/>
                    <input
                        type="image"
                        :src="require('../assets/paypal-checkout-logo-large.png')"
                        
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
        </v-layout>
    </v-container>
</template>

<script>
import axios from "axios";

export default {
    props: {
        /*order: {
            type: Object,
            required: true,
        },
        button: {
            type: Object,
            required: true,
        }*/
    },
    data: () => ({
        order: [
            {title: 'name', value: 'Ferdia SMC'},
            {title: 'email', value: 'sopermaf@tcd.ie'},
            {title: 'amount', value: '10.50'},
            {title: 'currency', value: 'USD'},
        ],
        button: {
            url: 'example.com',
        },
    }),
    methods: {
        cancelOrder() {
            axios.post('/payments/cancel/');
            this.$emit("pageSelection", "BOOKING");
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
</style>