<template>
  <v-container>
    <v-layout text-center wrap justify-center>

      <v-flex ma-5 lg12 xs12>
        <h3 class="display-1 font-weight-light mb-3">
          <span>Learn</span>
          <span class="font-weight-bold font-italic">
            Real
          </span>
          <span>English</span>
        </h3>
      </v-flex>

      <div class="break" />

      <v-flex lg7 md8 sm10 xs12 >
          <p>
            Do you want to speak English
            <span class="font-weight-bold">fluently</span>
            and
            <span class="font-weight-bold">confidently</span>
            ?
            Do you want to improve your listening and pronunciation?

            Here at Polyglossa, our mission is to help you do exactly
            that!
            We want to help you speak English the way Americans really speak.
            In our English seminars, you will learn how to:
          </p>
      </v-flex>
      
      <div class="break" />

      <v-flex ma-2 lg2 md4 sm2 xs5 text-left>
          <ul>
            <li class="font-weight-bold">
              increase your fluency
            </li>
            <li class="font-weight-bold">
              improve your listening skills
            </li>
          </ul>
      </v-flex>

      <v-flex ma-2 lg3 md5 sm3 xs6 text-left>
          <ul>
            <li class="font-weight-bold">
              speak with correct pronunciation
            </li>
            <li class="font-weight-bold">
              use native expressions
            </li>
          </ul>
      </v-flex>

      <div class="break" />

      <v-flex lg7 md8 sm10 xs12 ma-5>
          <p>
            If you want to speak English better and understand more, join one of our seminars today!
          </p>
      </v-flex>

      <div class="break" />

      <!-- Seminars -->
      <v-col
        lg="3"
        sm="4"
      >
        <h2 class="mb-2">Top Seminar Types</h2>
        <v-card
          hover
          v-for="sem in highlightedSeminars"

          :key="sem.title"
          class="mb-2 mr-2"
          @click="changePage('COURSES')"
        >
          <v-card-text
          >
           <b> {{sem.title}} </b>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Calendar -->
      <v-col
        sm="4"
        lg="3"
      >
        <h2 class="mb-3">Upcoming Seminars</h2>
        <v-card
          v-for="slotDate in upcomingSlots"
          :key="slotDate.date"
          class="mb-2"
        >
          <v-card-title
            class="font-weight-black"
          >
            {{slotDate.date}}
          </v-card-title>
          
          <v-list>
            <v-list-item
              v-for="seminar in slotDate.seminars"
              :key="seminar"
              dense
              class="text-left"
              @click="changePage('BOOKING')"
            >
              <v-list-item-title>
                {{seminar}}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <div class="break" />

      <!-- Overview Video -->
      <v-flex ma-5 xs12 lg7>
          <iframe
            class="framed"
            src="https://www.youtube.com/embed/Z4oozQpgmsw"
            frameborder="0"
            style="width: 100%"
            height="300"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
          </iframe>
      </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  props: {
    seminars: {
      type: Array,
      required: true,
    }
  },
  data: () => ({
    upcomingSlots: [],
  }),
  mounted() {
    axios.get('/classes/get/seminars/upcoming/').then(reponse => {
      this.upcomingSlots = reponse.data;
    })
  },
  methods: {
    changePage(destinationPage) {
      this.$emit("pageSelection", destinationPage);
    }
  },
  computed: {
    highlightedSeminars: function() {
      return this.seminars.filter(function(sem) { return sem.is_highlighted})
    }
  }
};
</script>

<style scoped>

.framed {
  border: 3px solid black;
}

</style>