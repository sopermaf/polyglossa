<template>
    <v-footer 
      app
      height="auto"
      elevation="10" 
      secondary
      absolute
    >
      <v-layout text-center row wrap>
        <v-flex  py-3 text-xs-center md12>
          <span class="font-weight-light">
            &copy; {{ new Date().getFullYear() }} — 
            <strong>Polyglossa</strong>
          </span>
        </v-flex>
      </v-layout>
    </v-footer>
</template>