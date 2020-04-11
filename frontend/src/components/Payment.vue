<template>
    <v-container>
        <v-layout justify-center wrap text-center class="mx-auto">
            <v-flex ma-5 lg6 s4 xs12>
                <h1> Continue to Paypal </h1>
                <form action="https://www.sandbox.paypal.com/cgi-bin/webscr" method="post">
                    <input type="hidden" name="cmd" value="_s-xclick" />
                    <input type="hidden" name="encrypted" :value="button_address"/>
                    <input
                        type="image"
                            src="https://www.paypalobjects.com/webstatic/en_US/i/buttons/checkout-logo-large.png"
                        
                        border="0"
                        name="submit"
                        alt="Check out with PayPal"
                    />
                </form>
            </v-flex>
        </v-layout>
    </v-container>

    

</template>

<script>
import axios from "axios";

export default {
    data: () => ({
        button_address: null,
    }),
    mounted() {
        axios.get('/payments/button/').then(response => {
            console.log(response.data);
            this.button_address = response.data['button'];
        })
    },
};
</script>