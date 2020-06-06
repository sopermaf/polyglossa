<template>
  <v-app>
    <!-- Header -->
    <PolyToolbar @pageSelection="updateView" @drawer="drawerVisible"/>

    <!-- Page Content -->
    <v-content>
      <v-navigation-drawer
        v-model="drawer"
        absolute
        temporary
      >
        <v-list-item>
          <v-list-item-avatar>
            <v-img src="https://randomuser.me/api/portraits/men/78.jpg"></v-img>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title>John Leider</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list dense>

          <v-list-item
            v-for="item in items"
            :key="item.title"
            link
          >
            <v-list-item-icon>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>

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
    drawer: false,
    items: [
      {title: 'helloworld', icon: 'house'}
    ]
  }),
  methods: {
    updateView(view) {
      this.pageSelection = view;
    },
    drawerVisible(val) {
      this.drawer = val;
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
