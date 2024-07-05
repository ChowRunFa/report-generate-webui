const menus = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
    meta: {
      title: '首页',
      icon: 'menu',
      showMenu: true
    }
  },
  {
    path: '/doc',
    name: 'doc',
    component: () => import('@/views/Documents.vue'),
    meta: {
      title: '文档',
      icon: 'collection',
      showMenu: true
    }
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/views/AboutView.vue'),
    meta: {
      title: '关于',
      icon: 'about',
      showInbreadcrumb: true,
      showMenu: false
    }
  },
  {
    path: '/user',
    name: 'user',
    meta: {
      title: '报告生成',
      icon: 'tickets',
      showMenu: true
    },
    children: [
      {
        path: '/user/list',
        name: 'userList',
        component: () => import('@/views/user/List.vue'),
        meta: {
          title: '文献报告',
          icon: 'memo',
          showMenu: true
        }
      },
      {
        path: '/user/portrait',
        name: 'userPortrait',
        component: () => import('@/views/user/Portrait.vue'),
        meta: {
          title: '综合报告',
          icon: 'document',
          showMenu: true
        }
      },
      {
        path: '/user/patent',
        name: 'userPatent',
        component: () => import('@/views/user/Patent.vue'),
        meta: {
          title: '文献综述',
          icon: 'notebook',
          showMenu: true
        }
      }
    ]
  },
  {
    path: '/multi',
    name: 'multi',
    meta: {
      title: '检索增强',
      icon: 'ZoomIn',
      showMenu: true
    },
    children: [
      {
        path: '/multi/two',
        name: 'multiTwo',
        // component: () => import('@/views/multi/ConsKG.vue'),
        meta: {
          title: '知识图谱',
          icon:'Share',
          showMenu: true
        },
        children: [
          {
            path: '/multi/two/ConsKG',
            name: 'multiTwoConsKG',
            component: () => import('@/views/multi/ConsKG.vue'),
            meta: {
              title: '图谱构建',
              icon:'Aim',
              showMenu: true
            },
          }, {
            path: '/multi/two/KGRepo',
            name: 'multiTwoKGRepo',
            component: () => import('@/views/multi/KGRepo.vue'),
            meta: {
              title: '图谱报告',
              icon:'SetUp',
              showMenu: true
            },

          }

        ]
      }
    ]
  },
  {
    path: '/admin',
    name: 'admin',
    meta: {
      title: '质量评估',
      icon: 'DataAnalysis',
      showMenu: true
    },
    children: [
      {
        path: '/admin/list',
        name: 'adminList',
        component: () => import('@/views/admin/List.vue'),
        meta: {
          title: '文本质量',
          icon: 'Money',
          showMenu: true
        }
      }
    ]
  },
  {
    path: '/sys',
    name: 'sys',
    component: () => import('@/views/Sys.vue'),
    meta: {
      title: '系统设置',
      icon: 'setting',
      showMenu: true
    }
  },
  {
    path: '/404',
    name: 'NotFound',
    component: () => import('@/views/404.vue')
  }
]
export default menus
