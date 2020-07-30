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
                <v-row>
                    <v-col
                        lg="12"
                        sm="4"
                    >
                        <h2> Exercises </h2>
                        <v-card
                            v-for="exercise in item.exercises"
                            :key="exercise"
                            class="mb-2 d-flex-inline"
                        >
                            {{exercise}}
                        </v-card>
                    </v-col>
                <!--</v-row>
                <v-row>-->
                    <v-col
                        lg="4"
                        sm="12"
                    >
                        <h2> Videos </h2>
                        <v-card
                            v-for="video in item.videos"
                            :key="video"
                            class="mb-2 d-flex-inline"
                        >
                            {{video}}
                        </v-card>
                    </v-col>
                <!--</v-row>
                <v-row>-->
                    <v-col
                        lg="4"
                        sm="12"
                    >
                        <h2> Readings </h2>
                        <v-card
                            v-for="reading in item.readings"
                            :key="reading"
                            class="mb-2 d-flex-inline"
                        >
                            {{reading}}
                        </v-card>
                    </v-col>

                </v-row>
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
            exercises: [
                "test",
                "test",
                "test",
            ],
            videos: [
                "test",
                "test",
                "test",
            ],
            readings: [
                "test",
                "test",
                "test",
            ],
        },
        {
            title: "A2",
            exercises: [
                "test",
                "test",
                "test",
            ],
            videos: [
                "test",
                "test",
                "test",
            ],
            readings: [
                "test",
                "test",
                "test",
            ],
        },
        {
            title: "B1",
            exercises: [
                "test",
                "test",
                "test",
            ],
            videos: [
                "test",
                "test",
                "test",
            ],
            readings: [
                "test",
                "test",
                "test",
            ],
        },
        {
            title: "B2",
            exercises: [
                "test",
                "test",
                "test",
            ],
            videos: [
                "test",
                "test",
                "test",
            ],
            readings: [
                "test",
                "test",
                "test",
            ],
        },
        {
            title: "C1",
            exercises: [
                "test",
                "test",
                "test",
            ],
            videos: [
                "test",
                "test",
                "test",
            ],
            readings: [
                "test",
                "test",
                "test",
            ],
        },
    ]
  }),
};
</script>

<style>

</style>