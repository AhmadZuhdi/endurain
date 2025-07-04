<template>
	<div class="bg-body-tertiary shadow-sm rounded p-3">
		<div class="row justify-content-center align-items-center">
			<div class="col d-none d-lg-block">
				<img width="auto" height="auto" :src="loginPhotoUrl" alt="Square login image" class="img-fluid rounded" v-if="serverSettingsStore.serverSettings.login_photo_set" />
				<img width="auto" height="auto" src="/src/assets/login.png"  alt="Square login image" class="img-fluid rounded" v-else >
			</div>
			<div class="col form-signin text-center m-3">
				<form @submit.prevent="submitForm">
					<h1>Endurain</h1>
					<p>{{ $t("loginView.subtitle") }}</p>
					<br>

					<div class="form-floating">
						<input type="text" class="form-control" id="floatingInput" name="loginUsername" :placeholder='$t("loginView.username")' v-model="username" required>
						<label for="loginUsername">{{ $t("loginView.username") }}</label>
					</div>
					<br>
					<div class="form-floating position-relative">
						<input :type="showPassword ? 'text' : 'password'" class="form-control" name="loginPassword" :placeholder='$t("loginView.password")' v-model="password" required>
						<label for="loginPassword">{{ $t("loginView.password") }}</label>
						<button type="button" class="btn position-absolute top-50 end-0 translate-middle-y me-2" @click="togglePasswordVisibility">
							<font-awesome-icon :icon="showPassword ? ['fas', 'eye-slash'] : ['fas', 'eye']" />
						</button>
					</div>
					<br>
					<button class="w-100 btn btn-lg btn-primary" type="submit">{{ $t("loginView.signInButton") }}</button>
					<!--<div>
						<hr>
						<button class="w-100 btn btn-lg btn-warning disabled" type="submit">{{ $t("loginView.signUpButton") }}</button>
					</div>-->
				</form>
			</div>
		</div>
	</div>
</template>

<script setup>
// Importing the vue composition API
import { ref, onMounted } from "vue";
// Importing the router
import { useRoute, useRouter } from "vue-router";
// Importing the i18n
import { useI18n } from "vue-i18n";
// Import Notivue push
import { push } from "notivue";
// Importing the stores
import { useAuthStore } from "@/stores/authStore";
import { useServerSettingsStore } from "@/stores/serverSettingsStore";
// Importing the services for the login
import { session } from "@/services/sessionService";
import { profile } from "@/services/profileService";

// Variables
const route = useRoute();
const router = useRouter();
const { locale, t } = useI18n();
const username = ref("");
const password = ref("");
const authStore = useAuthStore();
const serverSettingsStore = useServerSettingsStore();
const showPassword = ref(false);
const loginPhotoUrl = serverSettingsStore.serverSettings.login_photo_set
	? `${window.env.ENDURAIN_HOST}/server_images/login.png`
	: null;

// Toggle password visibility
const togglePasswordVisibility = () => {
	showPassword.value = !showPassword.value;
};

// Handle the form submission
const submitForm = async () => {
	// Create the form data
	const formData = new URLSearchParams();
	formData.append("grant_type", "password");
	formData.append("username", username.value);
	formData.append("password", password.value);

	try {
		// Get the token
		const session_id = await session.authenticateUser(formData);

		// Get logged user information
		const userProfile = await profile.getProfileInfo();

		// Store the user in the auth store
		authStore.setUser(userProfile, session_id, locale);

		// Redirect to the home page
		return router.push("/");
	} catch (error) {
		// Handle the error
		if (error.toString().includes("401")) {
			push.error(`${t("loginView.error401")} - ${error}`);
		} else if (error.toString().includes("403")) {
			push.error(`${t("loginView.error403")} - ${error}`);
		} else if (error.toString().includes("500")) {
			push.error(`${t("loginView.error500")} - ${error}`);
		} else {
			push.error(`${t("loginView.errorUndefined")} - ${error}`);
		}
	}
};

onMounted(() => {
	// Check if the session expired
	if (route.query.sessionExpired === "true") {
		push.warning(t("loginView.sessionExpired"));
	}
	// Check if the logout was successful
	if (route.query.logoutSuccess === "true") {
		push.success(t("loginView.logoutSuccess"));
	}
	// Check if the public activity was not found
	if (route.query.errorPublicActivityNotFound === "true") {
		push.error(t("loginView.errorPublicActivityNotFound"));
	}
	// Check if the public shareable links are disabled
	if (route.query.errorpublic_shareable_links === "true") {
		push.error(t("loginView.errorpublic_shareable_links"));
	}
});
</script>
