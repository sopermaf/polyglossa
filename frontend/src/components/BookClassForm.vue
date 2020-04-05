<template>
  <v-container>
    <v-layout justify-center wrap text-center class="mx-auto">
      <v-flex md-5 lg6 s4 xs12>
        <v-form ref="form" v-model="valid" lazy-validation>
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

          <!-- Validate Form -->
          <v-btn
            :disabled="!valid"
            color="success"
            class="mr-4"
            @click="validate"

          >
            Continue to payment
          </v-btn>

          <!-- Reset Form -->
          <v-btn
            color="error"
            class="mr-4"
            @click="reset"
          >
            Reset Form
          </v-btn>
        </v-form>
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
      type: Object
    }
  },
  data: () => ({
    valid: true,
    bookingName: null,
    bookingEmail: null,
    seminarChoice: null,
    bookingChoice: null,
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
    seminars: [],
    slots: [],
  }),
  mounted() {
    axios.get('/book_class/get/activities/SEM').then(response => {
      this.seminars = response.data['activities'];
    })
    this.seminarChoice = this.prefilledChoice;
  },
  watch: {
    'seminarChoice': {
      handler: function(after, before){
        this.getSlots(after.id);
      }
    }
  },
  methods: {
    postData() {
      axios.post('/book_class/signup/seminar', qs.stringify({
        student_name: this.bookingName,
        student_email: this.bookingEmail,
        slot_id: this.bookingChoice.id,
      }))
      .then(function (response) {
        window.location.assign(response.request.responseURL);
      })
      .catch(function (error) {
        console.log(error);
      });
    },
    validate () {
        if (this.$refs.form.validate()) {
            this.snackbar = true;
            this.postData();
            this.$refs.form.reset();
        }
        this.snackbar = true;
        //console.log(this.bookingChoice);
    },
    reset () {
      this.$refs.form.reset()
    },
    getSlots(id) {
      axios.get('/book_class/get/seminar_slots/' + id).then(response => {
        this.slots = response.data["slots"] || [];
      })
    },
    displaySlotDetails(slot) {
      var moment = require('moment');
      
      var datetimeStr = moment(slot.start_datetime).format("DD MMM hh:mm a");

      return `${datetimeStr} (${slot.duration_in_mins} mins)`;
    }
  },
}
</script>