<template>
  <v-container>
    <v-layout text-center wrap justify-center>
        <h1 class="m-4">
            Learning Materials
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
                :key="level.title"
                class="d-flex-3"
            >
                {{level.title}}
            </v-tab>
        </v-tabs>

        <v-tabs-items
            v-model="tab"
            style="height: 500px; width: 100%;"
        >
            <v-tab-item
                v-for="item in learingMaterials"
                :key="item.title"
            >
                <!-- Show all for larger screens -->
                <v-row
                    justify="center"
                    class="hidden-sm-and-down"
                >
                    <v-col
                        cols="4"
                        v-for="(data, title) in item.content"
                        :key="title"
                        class="mt-2"
                    >
                        <h2> {{title}} </h2>
                        <v-card
                            v-for="download in data"
                            :key="download.link"
                            class="mb-2 d-flex-inline"
                            :href="download.link"
                        >
                            {{download.title}}
                        </v-card>
                    </v-col>
                </v-row>

                <!-- Expansion panels for small screens -->
                <v-expansion-panels
                    class="hidden-md-and-up"
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
                                    class="mb-1"
                                    hover
                                >
                                    {{download.title}}
                                </v-card>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                </v-expansion-panels>
            </v-tab-item>
        </v-tabs-items>

    </v-layout>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    tab: null,
    learingMaterials: [
        {
            title: "A1",
            content:{
                exercises: [
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                    {title: "exercise", link: "http://google.com"},
                ],
                videos: [
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                    {title: "video", link: "http://google.com"},
                ],
                readings: [
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                    {title: "reading", link: "http://google.com"},
                ]
            }
        },
        {title: "A2", content: {exercises: [], videos: [], readings: []}},
        {title: "B1", content: {exercises: [], videos: [], readings: []}},
        {title: "B2", content: {exercises: [], videos: [], readings: []}},
        {title: "C1", content: {exercises: [], videos: [], readings: []}},
    ]
  }),
};
</script>

<style>

</style>