<template>

    <v-hover v-slot:default="{ hover }" open-delay>

        <v-card  
            outlined
            :elevation="hover ? 16: 2" 
        >
            <v-card-title class="justify-center mx-auto"> {{sem.title}} - ${{sem.price}} </v-card-title>
            <v-card-text> {{sem.description}} </v-card-text>
            <v-card-actions class="justify-center mx-auto" >
            <v-expand-transition>
                <v-btn
                    v-if="hover"
                    @click="chooseCourse()"
                    class="d-flex transition-fast-in-fast-out v-card--reveal"
                >
                    Book Now
                </v-btn>
            </v-expand-transition>
            </v-card-actions>
        </v-card>
    </v-hover>

</template>

<script>
export default {
    props: {
        sem: {
            type: Object
        }
    },
    data: () => ({
        buttonShow: false
    }),
    methods: {
        chooseCourse(){
            this.$emit("courseChoice", this.sem);
        }
    }
};
</script>