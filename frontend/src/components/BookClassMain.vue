<template>
  <v-container>
    <v-layout text-center wrap>

      <v-flex mb-4 xs12>
        <h2 class="headline font-weight-bold mb-3">
          Select your class slot below
          </h2>
      </v-flex>
      
      
      <v-flex mb-4 xs12>
        
        <p>Selected Time: {{ time }}</p>
        <p>Selected Date: {{ date }}</p>
      </v-flex>

      <v-flex ma-4 xs5 center>
        <v-date-picker
          v-model="date"
          color="green lighten-1"
        ></v-date-picker>
      </v-flex>

      <v-flex ma-4 xs5>
         <v-time-picker
          v-model="time"
          format="24hr"
          :allowed-hours="dailyHours"
          :allowed-minutes="minuteInterval"
          :landscape="$vuetify.breakpoint.mdAndUp"
          class="mt-4"
          full-width
          type="month"
        ></v-time-picker>
      </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    time: "",
    date: "",
    dailyHours: [13,14,15],
    minuteInterval:[0,30]
  }),
};
</script>
