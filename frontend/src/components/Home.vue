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
        lg="6"
        sm="4"
      >
        <h2 class="mb-2">Top Seminar Types</h2>
        <v-card
          hover
          v-for="sem in seminars"
          :key="sem.title"
          class="mb-2 mr-2"
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
        lg="6"
      >
        <h2 class="mb-3">Upcoming Seminars</h2>
        <v-card
          v-for="slotDate in upcomingSlots"
          :key="slotDate.date"
          class="mb-2"
        >
          <v-card-title>
            {{slotDate.date}}
          </v-card-title>
          
          <v-list>
            <v-list-item
              v-for="slotType in slotDate.slotTypes"
              :key="slotType"
            >
              <v-list-item-title>
                {{slotType}}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>


    </v-layout>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    seminars: [
      {id: 0, title: "Grammar Essentials \"get\"", description: "name", price: 10.5},
      {id: 1, title: "English Pronunciation", description: "name", price: 10.5},
      {id: 2, title: "Phrasal Verbs", description: "name", price: 10.5},
      {id: 3, title: "Free Trial Seminar!", description: "Free Seminar!", price: 0.0},
    ],
    upcomingSlots: [
      {
        date: "July 10th",
        slotTypes: [
          "Grammar Essentials \"get\"",
          "English Pronunciation",
        ]
      },
      {
        date: "July 11th",
        slotTypes: [
          "Phrasal Verbs",
          "English Pronunciation",
        ]
      },
      {
        date: "July 12th",
        slotTypes: [
          "Phrasal Verbs",
          "Beginner English",
        ]
      },
    ]
  }),
};
</script>
