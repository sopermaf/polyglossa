<template>
  <v-container>
    <v-layout text-center wrap justify-center>
        <h1> Contact Us </h1>
        
        <div class="break" />

        <v-flex ma-5 lg7 s12 xs12>
            <p>
                For any inquiries, questions, or problems,
                please send an email to help@polyglossa.com.
            </p>
            <p>
                Check out our social media channels for more English tips, lessons, and practice.
            </p>
        </v-flex>

        <div class="break" />

        <h1> Social Media </h1>

        <div class="break" />

        <v-flex ma-5 lg4 md4 s4 xs12 >
            <v-list>
                <v-list-item
                    v-for="social in socialMedia" :key="social.title"
                    :href="social.link"
                    flat
                >
                    <v-list-item-avatar>
                        <v-img :src="social.image" href="google.com" />
                    </v-list-item-avatar>

                    <v-list-item-content>
                        <v-list-item-title>{{ social.detail }}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  props: {
      socialMedia: {
          type: Array,
          required: true,
      }
  },
  data: () => ({
    contactDetails: [
      {name: 'Email', data: 'example@polyglossa.com'},
    ],
  }),
};
</script>
