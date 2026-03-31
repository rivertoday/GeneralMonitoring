/**
 * 用户状态管理
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { UserInfo } from '../types'

export const useUserStore = defineStore('user', () => {
  // 状态
  const currentUser = ref<UserInfo | null>(null)
  const userList = ref<UserInfo[]>([])

  // 设置当前用户
  function setCurrentUser(user: UserInfo | null) {
    currentUser.value = user
  }

  // 设置用户列表
  function setUserList(users: UserInfo[]) {
    userList.value = users
  }

  // 添加用户
  function addUser(user: UserInfo) {
    userList.value.push(user)
  }

  // 更新用户
  function updateUser(user: UserInfo) {
    const index = userList.value.findIndex((u) => u.id === user.id)
    if (index !== -1) {
      userList.value[index] = user
    }
    if (currentUser.value?.id === user.id) {
      currentUser.value = user
    }
  }

  // 删除用户
  function removeUser(userId: number) {
    userList.value = userList.value.filter((u) => u.id !== userId)
    if (currentUser.value?.id === userId) {
      currentUser.value = null
    }
  }

  // 根据ID获取用户
  function getUserById(userId: number): UserInfo | undefined {
    return userList.value.find((u) => u.id === userId)
  }

  return {
    // 状态
    currentUser,
    userList,
    // 方法
    setCurrentUser,
    setUserList,
    addUser,
    updateUser,
    removeUser,
    getUserById,
  }
})

