import { createStore } from 'vuex'

export default createStore({
  state: {
    lang: sessionStorage.getItem('lang') || 'en',
    user: JSON.parse(localStorage.getItem('user') || 'null') // null vagy {username, email, role}
  },
  getters: {
    lang: state => state.lang,
    user: state => state.user,
    isAdmin: state => state.user && state.user.role === 'admin',
    isChief: state => state.user && state.user.role === 'chief',
    isWorker: state => state.user && state.user.role === 'worker',
    isCrew: state => state.user && state.user.role === 'crew',
    isLoggedIn: state => !!state.user
  },
  mutations: {
    SET_LANG(state, lang) {
      state.lang = lang
      sessionStorage.setItem('lang', lang)
    },
    SET_USER(state, user) {
      state.user = user
      if (user) {
        localStorage.setItem('user', JSON.stringify(user))
        // opcionális, ha sessionStorage-be is akarod:
        // sessionStorage.setItem('user', JSON.stringify(user))
      } else {
        localStorage.removeItem('user')
        sessionStorage.removeItem('user') // ha netán ott is volt!
      }
    }
  },
  actions: {
    setLang({ commit }, lang) {
      commit('SET_LANG', lang)
    },
    setUser({ commit }, user) {
      commit('SET_USER', user)
    },
    logout({ commit }) {
      // Tokenek törlése minden storage-ból
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      sessionStorage.removeItem('access_token')
      sessionStorage.removeItem('refresh_token')
      // User törlése storage-ból is
      localStorage.removeItem('user')
      sessionStorage.removeItem('user')
      // Store törlés
      commit('SET_USER', null)
    }
  },
  modules: {}
})
