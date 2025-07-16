import {
	fetchGetRequest
} from "@/utils/serviceUtils";

export const activitiesEfforts = {
    getUserEfforts(
        activityType,
        interval = "monthly"
    ) {
        return fetchGetRequest(`activities/efforts?activity_type=${activityType}&interval=${interval}`);
    }
}