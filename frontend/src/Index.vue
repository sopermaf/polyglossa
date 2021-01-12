<template>
  <v-app>
    <!-- Header -->
    <PolyToolbar
      @pageSelection="updateView"
      @drawer="drawerVisible"
      :switchPoint="breakPoint"
      :isSPAToolbar="true"
    />

    <!-- Page Content -->
    <v-content>
      
      <v-navigation-drawer
        v-model="drawer"
        absolute
        temporary
        :class="`d-flex d-${breakPoint}-none`"
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
              <v-img :src="item.image"></v-img>
            </v-list-item-avatar>

            <v-list-item-content>
              <v-list-item-title>{{item.title}}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-navigation-drawer>

      <template v-if="pageSelection == 'HOME'">
        <Home
          :seminars="seminars"
          @pageSelection="updateView"
        />
      </template>
      <template v-else-if="pageSelection == 'COURSES'">
        <Courses
          :seminars="seminars"
          @courseChoice="prefillForm"
        />
      </template>
      <template v-else-if="pageSelection == 'BOOKING'">
        <BookClassForm
          :prefilledChoice="courseChoice"
          :seminars="seminars"
          :crsf="crsf"
          @pageSelection="updateView"
          @orderGenerated="orderUpdate"
          @buttonGenerated="updateButton"
        />
      </template>
      <template v-else-if="pageSelection == 'LEARNING'">
        <Learning />
      </template>
      <template v-else-if="pageSelection == 'CONTACT_US'">
        <ContactUs :socialMedia="socialMediaItems"/>
      </template>
      <template v-else-if="pageSelection == 'ABOUT_US'">
        <AboutUs />
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
import ContactUs from "./components/ContactUs.vue";
import AboutUs from "./components/AboutUs.vue";
import Learning from "./components/Learning.vue";
import {mdiHome, mdiBookOpenPageVariant, mdiClipboardEditOutline, mdiInformationVariant, mdiBookshelf, mdiCommentTextMultiple } from '@mdi/js'
import axios from "axios";

export default {
  name: "Index",
  components: {
    Home,
    Courses,
    BookClassForm,
    PolyToolbar,
    PolyFooter,
    ContactUs,
    AboutUs,
    Learning,
  },
  data: () => ({
    pageSelection: "HOME",
    breakPoint: 'lg',
    courseChoice: null,
    drawer: false,
    isNavBarVisible: false,
    seminars: [],
    crsf: null,
    
    navItems: [
      {title: 'Home', icon: mdiHome, pageSelection: "HOME"},
      {title: 'Seminars Types', icon: mdiBookOpenPageVariant, pageSelection: "COURSES"},
      {title: 'Join a Seminar', icon: mdiClipboardEditOutline, pageSelection: "BOOKING"},
      {title: 'Learning Materials', icon: mdiBookshelf, pageSelection: "LEARNING"},
      {title: 'About Us', icon: mdiInformationVariant, pageSelection: "ABOUT_US"},
      {title: 'Contact Us', icon: mdiCommentTextMultiple, pageSelection: "CONTACT_US"},
    ],
    socialMediaItems: [
      {
        title: 'Youtube',
        detail: 'Conner Ingles',
        link: 'https://www.youtube.com/conneringles',
        icon: 'https://w7.pngwing.com/pngs/963/811/png-transparent-youtube-logo-youtube-red-logo-computer-icons-youtube-television-angle-rectangle.png',
        image: 'https://image.flaticon.com/icons/svg/174/174883.svg',
      },
      {
        title: 'Instagram',
        detail: '@polyglossalanguages',
        link: 'https://www.instagram.com/polyglossalanguages/',
        icon: 'https://p7.hiclipart.com/preview/477/609/118/logo-computer-icons-clip-art-instagram-logo.jpg',
        image: 'https://image.flaticon.com/icons/svg/1409/1409946.svg',
      },
    ],
  }),
  mounted() {
    axios.get('/classes/get/activities/SEM').then(response => {
      this.seminars = response.data['activities'];
      this.crsf = response.data['token'];
    })
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