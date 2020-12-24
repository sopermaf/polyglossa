<template>

    <v-hover v-slot:default="{ hover }" open-delay>

        <v-card  
          outlined
          :elevation="hover ? 16: 2" 
        >
          <v-card-title
            class="word-break-keep-all justify-center"
          > 
            {{sem.title}}
            <br>
            ${{sem.price}}
          </v-card-title>
          
          <!-- pre-wrap used to ensure line-breaks from TextField -->
          <v-card-text
            class="justify-left"
            style="white-space: pre-wrap;"
          >
            {{ sem.description }}
          </v-card-text>
          
          <v-card-actions
            class="justify-center"
          >
            <v-btn
              @click="chooseCourse()"
              class="d-flex transition-fast-in-fast-out v-card--reveal"
            >
              Sign Up
            </v-btn>
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

<style>
.word-break-keep-all {
  word-break: keep-all;
}
</style>