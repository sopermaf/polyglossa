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

    <!-- Lesson Type -->
    <v-select
      v-model="lessonChoice"
      :items="lessonOptions"
      :rules="[v => !!v || 'Lesson Type is required']"
      label="Lesson Type"
      required
    ></v-select>

    <!-- Time Slot -->
    <v-select
      v-model="bookingTime"
      :items="bookingTimeOptions"
      :rules="[v => !!v || 'Class Time is required']"
      label="Class Time"
      required
    ></v-select>

    <!-- Date Selection -->
    <v-menu
      ref="menu"
      v-model="menu"
      :close-on-content-click="false"
      :return-value.sync="date"
      transition="scale-transition"
      offset-y
      min-width="290px"
    >
      <template v-slot:activator="{ on }">
        <v-text-field
          v-model="date"
          label="Picker in menu"
          prepend-icon="event"
          readonly
          v-on="on"
        ></v-text-field>
      </template>
      <v-date-picker 
        v-model="bookingDate"
        no-title 
        scrollable
        :min="minDate"
        >
        
        <v-spacer></v-spacer>
        <v-btn text color="primary" @click="menu = false">Cancel</v-btn>
        <v-btn text color="primary" @click="$refs.menu.save(bookingDate)">OK</v-btn>
      </v-date-picker>
    </v-menu>

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
    menu: false,
    bookingName: '',
    nameRules: [
      v => !!v || 'Name is required',
    ],
    bookingEmail: '',
    emailRules: [
      v => !!v || 'E-mail is required',
      v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
    ],
    bookingTime: '',
    bookingTimeOptions: [
      '13:00',
      '14:00',
      '15:00',
    ],
    bookingDate: '',
    minDate: null,
    lessonOptions: null,
    lessonChoice: '',
  }),
  mounted() {
    this.setMinDate();

    this.page_load_data = document.body.getAttribute('data');
    console.log(this.page_load_data);
    this.lessonOptions = JSON.parse(this.page_load_data)['lesson_types'];

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
            this.postData();
            this.$refs.form.reset();
        }
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