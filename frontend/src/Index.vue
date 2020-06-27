<template>
  <v-app>
    <!-- Header -->
    <PolyToolbar
      @pageSelection="updateView"
      @drawer="drawerVisible"
      :isNavBarVisible="isNavBarVisible"
    />

    <!-- Page Content -->
    <v-content>
      
      <template
        v-if="isNavBarVisible">
        <v-navigation-drawer
          v-model="drawer"
          absolute
          temporary
        >
          <v-list >
            <!-- Navigation Items -->
            <v-list-item
              v-for="item in navItems"
              :key="item.title"
              @click="updateView(item.pageSelection)"
            >
              <v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-icon>

              <v-list-item-content>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>

          <v-divider></v-divider>
          <!-- Social Media Items -->
          <template
            v-for="item in socialMediaItems"
          >
            <v-list-item
              :key="item.title"
              :href="item.pageLink"
            >
              <v-list-item-avatar>
                <v-img :src="item.imageLink"></v-img>
              </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-title>{{item.title}}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>
        </v-navigation-drawer>
      </template>

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
import {mdiClipboardTextOutline, mdiHome, mdiBookOpenPageVariant } from '@mdi/js'

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
    isNavBarVisible: false,
    navItems: [
      {title: 'Home', icon: mdiHome, pageSelection: "HOME"},
      {title: 'Courses', icon: mdiBookOpenPageVariant, pageSelection: "COURSES"},
      {title: 'Book a class', icon: mdiClipboardTextOutline, pageSelection: "BOOKING"},
    ],
    socialMediaItems: [
      {
        title: 'Youtube',
        imageLink: 'https://w7.pngwing.com/pngs/963/811/png-transparent-youtube-logo-youtube-red-logo-computer-icons-youtube-television-angle-rectangle.png',
        pageLink: 'https://www.youtube.com/conneringles'
      },
      {
        title: 'Instagram',
        imageLink: 'https://p7.hiclipart.com/preview/477/609/118/logo-computer-icons-clip-art-instagram-logo.jpg',
        pageLink: 'https://www.instagram.com/polyglossalanguages/'
      },
    ]
  }),
  mounted() {
    if(window.innerWidth < 800){
      this.isNavBarVisible = true;
    }
  },
  methods: {
    updateView(view) {
      this.pageSelection = view;
      this.drawer = false;
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

<style>
.break {
  flex-basis: 100%;
  height: 0;
}
</style>