<template>
    <v-container>
        <v-layout justify-center wrap  class="mx-auto">
            <v-flex ma-5 lg7 s12 xs12>
                <v-card elevation="1">
                    <v-card-title>
                        Order Review
                    </v-card-title>
                    <ul class="no-bullets" ma-2>
                        <li v-for="(k, v) in order" :key="k">
                            <b>{{ v.toUpperCase() }}:</b> {{ k }}
                        </li>
                    </ul>
                    
                </v-card>
            </v-flex>
            <v-flex mt-2 lg5 s4 xs12 text-center>
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
            <v-flex mt-2 lg5 s4 xs12 text-center>
                <v-btn @click="cancelOrder" elevation="15">
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
        order: {
            name: 'Ferdia Soper Mac Cafraidh',
            email: 'sopermaf@tcd.ie',
            amount: 10.50,
            currency: 'USD'
        },
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

<style scoped>
ul.no-bullets {
  list-style-type: none;
  text-align: left;
}
</style>