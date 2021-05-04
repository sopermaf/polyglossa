<template>
  <v-container>
    <v-layout justify-center wrap text-center class="mx-auto">
      <v-flex md-5 lg6 s4 xs12>
        <h2>Seminar Signup Form</h2>
        <v-form ref="form" v-model="valid" lazy-validation class="elevation-4 pa-5">
          <!-- Name -->
          <v-text-field
            v-model="bookingName"
            :rules="nameRules"
            label="Name"
            required
          ></v-text-field>

          <!-- Email -->
          <v-text-field
            v-model="bookingEmail"
            :rules="emailRules"
            label="E-mail"
            required
          ></v-text-field>

          <!-- Seminar Type Selection -->
          <v-select :items="seminars" v-model="seminarChoice" label="Seminar Type" required :rules="notNullRules">
            <template slot="item" slot-scope="data">
              {{ data.item.title }} ${{ data.item.price }}
            </template>
            <template slot="selection" slot-scope="data">
              {{ data.item.title }} ${{ data.item.price }}
            </template>
          </v-select>

          <!-- Seminar Slot Selection -->
          <v-select :items="slots" v-model="bookingChoice" label="Seminar Slot" required :rules="notNullRules">
            <template slot="item" slot-scope="data">
              {{ displaySlotDetails(data.item) }}
            </template>
            <template slot="selection" slot-scope="data">
              {{ displaySlotDetails(data.item) }}
            </template>
          </v-select>

          <p class="grey--text text-subtitle-1">
            Seminars are available for 24 hours from the time listed
          </p>

          <!-- Validate Form -->
          <v-btn
            :disabled="!valid"
            color="success"
            class="mr-4 mb-2"
            @click="validate"
            mb-3
          >
            Continue to checkout
          </v-btn>

          <!-- Reset Form -->
          <v-btn
            color="error"
            class="mr-4 mb-2"
            @click="reset"
          >
            Reset Form
          </v-btn>
        </v-form>
      </v-flex>

      <v-flex
        ma-5
        lg12 s12 xs12
        class="grey--text text-subtitle-1"
      >
        <p> All times displayed in UTC. </p>
        
        <p> <b> UTC: </b> {{ utctime }} </p>

        <p> <b> Your local time: </b> {{ localtimezone }}</p>
      </v-flex>

      <v-flex
        ma-5
        lg12 s12 xs12
        class="red--text text-subtitle-1"
        v-if="errorMessage"
      >
        {{ errorMessage }}
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from "axios";
import qs from "qs";

export default {
  props: {
    prefilledChoice: {
      type: Object,
      required: true,
    },
    seminars: {
      type: Array,
      required: true,
    }
  },
  data: () => ({
    valid: true,
    bookingName: null,
    bookingEmail: null,
    seminarChoice: null,
    bookingChoice: null,
    requestResponse: null,
    crsfToken: null,
    errorMessage: null,
    localtimezone: null,

    // validation rules
    nameRules: [
      v => !!v || 'Name is required',
    ],
    emailRules: [
      v => !!v || 'E-mail is required',
      v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
    ],
    notNullRules: [
      v => !!v || 'Seminar choice required'
    ],
    slots: [],
  }),
  mounted() {
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.withCredentials = true

    this.seminarChoice = this.prefilledChoice;

    var moment = require('moment');
    this.localtimezone = moment().format('LT, ll');
    this.utctime = moment().utc().format('LT, ll');

  },
  watch: {
    'seminarChoice': {
      handler: function(seminar){
        this.getSlots(seminar.id);
      }
    }
  },
  methods: {
    postData() {
      // ensure error message unset
      this.errorMessage = null;

      axios.post('/classes/signup/seminar', qs.stringify({
        student_name: this.bookingName,
        student_email: this.bookingEmail,
        slot_id: this.bookingChoice.id,
        csrfMiddleWare: this.crsfToken
      }))
      .then(response => { // eslint-disable-line no-unused-vars
        window.location = '/payments/order/';
      })
      .catch(error => {
        // display error to user
        this.errorMessage = error.response.data;
      })
    },
    validate () {
        if (this.$refs.form.validate()) {
            this.snackbar = true;
            this.postData();
        }
        this.snackbar = true;
    },
    reset () {
      this.$refs.form.reset();
    },
    getSlots(id) {
      axios.get('/classes/get/seminar_slots/' + id).then(response => {
        this.slots = response.data["slots"] || [];
      })
    },
    displaySlotDetails(slot) {
      var moment = require('moment');
      
      var datetimeStr = moment(slot.start_datetime).format("DD MMM hh:mm a");

      return `${datetimeStr} (${slot.duration_in_mins} mins)`;
    },
  },
}
</script>