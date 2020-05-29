<template>
    <v-container>
        <v-layout justify-center wrap text-center class="mx-auto">
            <v-flex lg6 s4 xs12>
                <v-card elevation="10">
                    <v-card-title>
                        Order Review
                    </v-card-title>
                    <v-card-list>
                    <ul>
                        <li v-for="(k, v) in order" :key="k">
                            {{ v.toUpperCase() }} - {{ k }}
                        </li>
                    </ul>
                    </v-card-list>
                </v-card>
            </v-flex>
            <v-flex ma-5 lg6 s4 xs12>
                <v-form action="https://www.sandbox.paypal.com/cgi-bin/webscr" method="post">
                    <input type="hidden" name="cmd" value="_s-xclick" />
                    <input type="hidden" name="encrypted" :value="button.address"/>
                    <input
                        type="image"
                        :src="require('../assets/paypal-checkout-logo-large.png')"
                        
                        border="0"
                        name="submit"
                        alt="Check out with PayPal"
                    />
                </v-form>
            </v-flex>
            <v-flex lg6 s4 xs12>
                <v-btn @click="cancelOrder" elevation="15">
                    Cancel
                </v-btn>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
import axios from "axios";
import qs from "qs";

export default {
    props: {
        order: {
            type: Object,
            required: true,
        },
        button: {
            type: Object,
            required: true,
        }
    },
    data: () => ({
    }),
    methods: {
        cancelOrder() {
            axios.post('/payments/cancel/', qs.stringify({
                name: this.order.name,
                email: this.order.email,
            }))
            this.$emit("pageSelection", "BOOKING");
        },
    },
};
</script>