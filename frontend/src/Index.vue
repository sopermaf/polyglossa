<template>
  <v-app>
    <!-- Header -->
    <PolyToolbar @pageSelection="updateView" />

    <!-- Page Content -->
    <v-content>
      <template v-if="pageSelection == 'HOME'">
        <Home />
      </template>
      <template v-else-if="pageSelection == 'COURSES'">
        <Courses @courseChoice="prefillForm" />
      </template>
      <template v-else-if="pageSelection == 'BOOKING'">
        <BookClassForm
          :prefilledChoice="courseChoice"
          @pageSelection="updateView"
          @orderGenerated="orderUpdate"
          @buttonGenerated="updateButton"
        />
      </template>
      <template v-else-if="pageSelection == 'PAYMENT'">
        <Payment @pageSelection="updateView" :order="order" :button="button"/>
      </template>
    </v-content>

    <!-- Footer -->
    <PolyFooter />
  </v-app>
</template>

<script>
import Home from "./components/Home";
import Courses from "./components/Courses";
import BookClassForm from "./components/BookClassForm";
import PolyToolbar from "./components/PolyToolbar.vue";
import PolyFooter from "./components/PolyFooter.vue";
import Payment from "./components/Payment.vue"

export default {
  name: "Index",
  components: {
    Home,
    Courses,
    BookClassForm,
    PolyToolbar,
    PolyFooter,
    Payment,
  },
  data: () => ({
    pageSelection: "HOME",
    courseChoice: null,
    order: null,
    button: null,
  }),
  methods: {
    updateView(view) {
      this.pageSelection = view;
    },
    prefillForm(course) {
      this.pageSelection = "BOOKING";
      this.courseChoice = course;
    },
    orderUpdate(order) {
      this.order = order;
    },
    updateButton(button) {
      this.button = button;
    },
  }
};
</script>
