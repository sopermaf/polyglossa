<template>
  <v-form
    ref="form"
    v-model="valid"
    lazy-validation
  >

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

    <!-- Seminar Slot Selection -->
    <v-select :items="seminar_slots" v-model="bookingChoice" label="Seminar Slot" required :rules="seminarRules">
      <template slot="item" slot-scope="data">
        [{{ data.item.datetime_pretty }}] [{{ data.item.title }}] [${{ data.item.price }}] [{{ data.item.duration }}]
      </template>
      <template slot="selection" slot-scope="data">
        ({{ data.item.title }} {{ data.item.datetime_pretty }})
      </template>
    </v-select>

    <!-- Validate Form -->
    <v-btn
      :disabled="!valid"
      color="success"
      class="mr-4"
      @click="validate"

    >
      Submit
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
</template>

<script>
import axios from "axios";
import qs from "qs";

export default {
  data: () => ({
    valid: true,
    bookingName: null,
    bookingEmail: null,
    bookingChoice: null,
    // validation rules
    nameRules: [
      v => !!v || 'Name is required',
    ],
    emailRules: [
      v => !!v || 'E-mail is required',
      v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
    ],
    seminarRules: [
      v => !!v || 'Seminar choice required'
    ],
    seminar_slots: []
  }),
  mounted() {
    this.setMinDate();

    this.page_load_data = document.body.getAttribute('data');
    //console.log(this.page_load_data);
    this.seminar_slots = JSON.parse(this.page_load_data)['seminar_slots'];

    for(let i in this.seminar_slots){
      this.

      console.log(this.seminar_slots[i]);
    }

  },
  methods: {
    formatBookingDateTime() {
      return this.bookingDate + ' ' + this.bookingTime;
    },
    postData() {
      axios.post('/book_class/create/', qs.stringify({
        lesson_time: this.formatBookingDateTime(),
        student_name: this.bookingName,
        student_email: this.bookingEmail,
        lesson_type: this.lessonChoice,
      }))
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
    },
    validate () {
        if (this.$refs.form.validate()) {
            this.snackbar = true;
            //this.postData();
            this.$refs.form.reset();
        }
        this.snackbar = true;
        console.log(this.bookingChoice)
    },
    reset () {
      this.$refs.form.reset()
    },
    setMinDate() {
      var today = new Date(Date.now());
      this.minDate = today.toISOString().slice(0,10);
    },
  },
}
</script>