<template>
  <v-container>
    <v-layout text-center wrap justify-center>
        <h1 class="mb-4 mt-2">
            Learning Material
        </h1>
        <div class="break" />

        <v-tabs
            v-model="tab"
            color="primary mb-3"
            mobile-break-point
            centered
            grow
        >
            <v-tab
                v-for="level in learingMaterials"
                :key="level.level"
                class="d-flex-3"
            >
                {{level.level}}
            </v-tab>
        </v-tabs>

        <v-tabs-items
            v-model="tab"
            style="width: 100%;"
        >
            <v-tab-item
                v-for="item in learingMaterials"
                :key="item.title"
            >
                <!-- Side by side expansions for above XS -->
                <v-row
                    class="hidden-xs-only"
                >
                    <v-col
                        cols="4"
                        v-for="(data, title) in item.content"
                        :key="title"
                        class="mt-2"
                    >    
                        <v-expansion-panels
                        >
                            <v-expansion-panel>
                                <v-expansion-panel-header>
                                    <h3> {{title}} </h3>
                                </v-expansion-panel-header>
                                
                                <v-expansion-panel-content
                                >
                                    <v-card
                                        v-for="download in data"
                                        :key="download.link"
                                        class="mb-2 elevation-5"
                                        :href="download.link"
                                        target="_new"
                                        outlined
                                    >
                                        {{download.title}}
                                    </v-card>
                                </v-expansion-panel-content>
                            </v-expansion-panel>
                        </v-expansion-panels>
                    </v-col>
                </v-row>

                <!-- Connected Expansion Panels for XS screen -->
                <v-expansion-panels
                    class="hidden-sm-and-up"
                >
                    <v-col
                        cols="12"
                    >
                        <v-expansion-panel
                            v-for="(data, title) in item.content"
                            :key="title"
                            class="mt-2"
                        >
                            <v-expansion-panel-header>
                                <h3> {{title}} </h3>
                            </v-expansion-panel-header>
                            
                            <v-expansion-panel-content
                            >
                                <v-card
                                    v-for="download in data"
                                    :key="download.link"
                                    class="mb-2 elevation-15"
                                    :href="download.link"
                                    target="_new"
                                    outlined
                                >
                                    {{download.title}}
                                </v-card>
                            </v-expansion-panel-content>
                        </v-expansion-panel>
                    </v-col>
                </v-expansion-panels>
            </v-tab-item>
        </v-tabs-items>

    </v-layout>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data: () => ({
    tab: null,
    learingMaterials: []
  }),
  mounted() {
      axios.get('/materials/get-all').then(response => {
          this.learingMaterials = response.data;
      })
  }
};
</script>
