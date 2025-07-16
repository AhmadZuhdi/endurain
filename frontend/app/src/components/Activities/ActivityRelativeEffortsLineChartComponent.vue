<template>
<div style="height: 100%;">
    <div>
        <label for="interval">Interval</label>
        <select class="form-select" aria-label="interval select" id="interval"
                @change="loadEfforts"
                v-model="selectedInterval">
            <option v-for="interval in intervals" 
                :key="interval.value" 
                :value="interval.value" >
                {{ interval.label }}
            </option>
        </select>
    </div>
    <div style="height: 100%;">
        <canvas ref="chartCanvas"></canvas>
    </div>
</div>
</template>

<script setup>
import { defineProps, ref, onMounted, watch, computed } from "vue";
const props = defineProps({
    activityType: {
        type: Number,
        required: true
    },
    activityId: {
        type: Number,
        required: true
    }
});

import { useI18n } from "vue-i18n";
import { activitiesEfforts } from "@/services/activitiesEffortsService";

import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

const { t } = useI18n();

const chartCanvas = ref(null);
const activityActivityEfforts = ref([]);
const selectedInterval = ref('monthly');
let myChart = null;

const intervals = [
    { value: 'weekly', label: t("summaryView.optionWeekly") },
    { value: 'monthly', label: t("summaryView.optionMonthly") },
    { value: 'yearly', label: t("summaryView.optionYearly") },
]

const loadEfforts = async () => {
    try {
        activityActivityEfforts.value = await activitiesEfforts.getUserEfforts(
            props.activityType,
            selectedInterval.value
        );
    } catch (error) {
        console.error("Error loading efforts:", error);
    }
};

const computedChartData = computed(() => {

    if (activityActivityEfforts.value.length === 0) {
        return {
            labels: [],
            datasets: []
        };
    }

    const currentActivityEfforts = activityActivityEfforts.value.findIndex(effort => effort.activity_id == props.activityId);
    
    const higest = Math.max(...activityActivityEfforts.value.map(effort => effort.relative_effort));
    const lowest = Math.min(...activityActivityEfforts.value.map(effort => effort.relative_effort));
    
    const higestEffort = activityActivityEfforts.value.findIndex(effort => effort.relative_effort === higest);
    const lowestEffort = activityActivityEfforts.value.findIndex(effort => effort.relative_effort === lowest);
    
    const toSkip = [
        currentActivityEfforts,
        higestEffort,
        lowestEffort
    ];

    const activityEfforts = activityActivityEfforts.value
        .map((effort, x) => {
            return {
                x,
                y: effort.relative_effort,
            };
        })
        .filter((effort, i) => toSkip.indexOf(i) === -1);
    
    return {
        labels: [],
        datasets: [
            {
                label: t("activityMandAbovePillsComponent.labelGraphEfforts"),
                data: activityEfforts,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
            },
            {
                label: t("activityMandAbovePillsComponent.labelGraphEffortsHighest"),
                data: [
                    {
                        x: higestEffort,
                        y: activityActivityEfforts.value[higestEffort].relative_effort
                    }
                ],
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'red',
                fill: true,
            },

            {
                label: t("activityMandAbovePillsComponent.labelGraphEffortsLowest"),
                data: [
                    {
                        x: lowestEffort,
                        y: activityActivityEfforts.value[lowestEffort].relative_effort
                    }
                ],
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'green',
                fill: true,
            },

            {
                label: t("activityMandAbovePillsComponent.labelGraphEffortsCurrent"),
                data: [
                    {
                        x: currentActivityEfforts,
                        y: activityActivityEfforts.value[currentActivityEfforts].relative_effort
                    }
                ],
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'blue',
                fill: true,
            },
        ]
    };
});

watch(computedChartData, (newValue) => {
    if (!myChart) {
        return;
    }
    
    myChart.data = newValue
    myChart.update();
}, { deep: true });

onMounted(async () => {
    loadEfforts();

    myChart = new Chart(chartCanvas.value.getContext('2d'), {
        type: 'scatter',
        data: computedChartData.value,
        options: {
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.parsed.y}`;
                        }
                    }
                }
            },
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});

</script>