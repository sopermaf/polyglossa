<template>
  <v-form
    ref="form"
    v-model="valid"
    lazy-validation
  >

    <!-- Name -->
    <v-text-field
      v-model="name"
      :rules="nameRules"
      label="Name"
      required
    ></v-text-field>

    <!-- Email -->
    <v-text-field
      v-model="email"
      :rules="emailRules"
      label="E-mail"
      required
    ></v-text-field>

    <!-- Time Slot -->
    <v-select
      v-model="select_classTime"
      :items="classTime_options"
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
        v-model="date"
        no-title 
        scrollable
        :min="minDate"
        >
        
        <v-spacer></v-spacer>
        <v-btn text color="primary" @click="menu = false">Cancel</v-btn>
        <v-btn text color="primary" @click="$refs.menu.save(date)">OK</v-btn>
      </v-date-picker>
    </v-menu>

    <!-- Validate Form -->
    <v-btn
      :disabled="!valid"
      color="success"
      class="mr-4"
      @click="validate"
    >
      Validate
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
  export default {
    data: () => ({
      valid: true,
      menu: false,
      name: '',
      nameRules: [
        v => !!v || 'Name is required',
      ],
      email: '',
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      ],
      select_classTime: null,
      classTime_options: [
        '13:00',
        '14:00',
        '15:00',
      ],
      date: null,
      minDate: null,
    }),
    mounted() {
      this.setMinDate();
    },
    methods: {
      validate () {
        if (this.$refs.form.validate()) {
          this.snackbar = true
        }
      },
      reset () {
        this.$refs.form.reset()
      },
      setMinDate() {
        var today = new Date(Date.now());
        this.minDate = today.toISOString().slice(0,10);
      }
    },
  }
</script>