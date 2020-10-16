<template>
  <v-app>
    <!-- Header -->
    <PolyToolbar
      @pageSelection="updateView"
      @drawer="drawerVisible"
      :switchPoint="breakPoint"
      :isSPAToolbar="false"
    />

    <!-- Page Content -->
    <v-content>
      
      <iframe
        width="560"
        height="315"
        :src="video_id"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
      </iframe>

    </v-content>

    <!-- Footer -->
    <PolyFooter
    />
  </v-app>
</template>

<script>
import PolyToolbar from "./components/PolyToolbar.vue";
import PolyFooter from "./components/PolyFooter.vue";
import {mdiHome, mdiBookOpenPageVariant, mdiClipboardEditOutline, mdiInformationVariant, mdiBookshelf, mdiCommentTextMultiple } from '@mdi/js'

export default {
  name: "Video",
  components: {
    PolyToolbar,
    PolyFooter,
  },
  data: () => ({
    pageSelection: "HOME",
    breakPoint: 'lg',
    courseChoice: null,
    order: null,
    button: null,
    drawer: false,
    isNavBarVisible: false,
    seminars: [],
    crsf: null,
    video_id: "original",
    
    navItems: [
      {title: 'Home', icon: mdiHome, pageSelection: "HOME"},
      {title: 'Seminars Types', icon: mdiBookOpenPageVariant, pageSelection: "COURSES"},
      {title: 'Join a Seminar', icon: mdiClipboardEditOutline, pageSelection: "BOOKING"},
      {title: 'Learning Materials', icon: mdiBookshelf, pageSelection: "LEARNING"},
      {title: 'About Us', icon: mdiInformationVariant, pageSelection: "CONTACT_US"},
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
    this.video_id = "https://www.youtube.com/embed/" + document.body.getAttribute('video_id');
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