<template>
  <v-app>
    <!-- Header -->
    <PolyToolbar
      :isSPAToolbar="false"
    />

    <!-- Page Content -->
    <v-content>
      <v-container>
        <v-layout text-center wrap justify-center>
          <v-flex ma-5 xs12>
            <h1> {{ title }} </h1>
          </v-flex>

          <v-flex ma-5 xs12>

            <iframe
              v-if="error.length === 0"
              :src="video_id"
              frameborder="0"
              style="width: 100%"
              height="300"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
              allowfullscreen>
            </iframe>

            <div v-else>
              <h3> 
                  This seminar video is not available
                  <span v-if="error.includes('will be')"> yet </span> 
              </h3>
              <p class="red--text text-subtitle-1"> {{ error }} </p>
            </div>

          </v-flex>
        </v-layout>
      </v-container>
    </v-content>

    <!-- Footer -->
    <PolyFooter />
  </v-app>
</template>

<script>
import PolyToolbar from "./components/PolyToolbar.vue";
import PolyFooter from "./components/PolyFooter.vue";

export default {
  name: "Video",
  components: {
    PolyToolbar,
    PolyFooter,
  },
  data: () => ({
    video_id: "",
    title: "",
  }),
  mounted() {
    var videoInfo = JSON.parse(document.body.getAttribute('data'));

    this.video_id = 'https://www.youtube.com/embed/' + videoInfo.video_id;
    this.title = videoInfo.title;
    this.error = videoInfo.error;
  },
};
</script>
