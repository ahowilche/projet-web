-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : mar. 01 juil. 2025 à 08:29
-- Version du serveur : 10.4.28-MariaDB
-- Version de PHP : 8.1.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `gmycom`
--

-- --------------------------------------------------------

--
-- Structure de la table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'Agents');

-- --------------------------------------------------------

--
-- Structure de la table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add Historique de Transaction', 7, 'add_historiquetransaction'),
(26, 'Can change Historique de Transaction', 7, 'change_historiquetransaction'),
(27, 'Can delete Historique de Transaction', 7, 'delete_historiquetransaction'),
(28, 'Can view Historique de Transaction', 7, 'view_historiquetransaction'),
(29, 'Can add Remboursement', 8, 'add_remboursement'),
(30, 'Can change Remboursement', 8, 'change_remboursement'),
(31, 'Can delete Remboursement', 8, 'delete_remboursement'),
(32, 'Can view Remboursement', 8, 'view_remboursement'),
(33, 'Can add Compte', 9, 'add_compte'),
(34, 'Can change Compte', 9, 'change_compte'),
(35, 'Can delete Compte', 9, 'delete_compte'),
(36, 'Can view Compte', 9, 'view_compte'),
(37, 'Can add Crédit', 10, 'add_credit'),
(38, 'Can change Crédit', 10, 'change_credit'),
(39, 'Can delete Crédit', 10, 'delete_credit'),
(40, 'Can view Crédit', 10, 'view_credit'),
(41, 'Can add Mouvement', 11, 'add_mouvement'),
(42, 'Can change Mouvement', 11, 'change_mouvement'),
(43, 'Can delete Mouvement', 11, 'delete_mouvement'),
(44, 'Can view Mouvement', 11, 'view_mouvement'),
(45, 'Can add Client', 12, 'add_client'),
(46, 'Can change Client', 12, 'change_client'),
(47, 'Can delete Client', 12, 'delete_client'),
(48, 'Can view Client', 12, 'view_client'),
(49, 'Can add Document Client', 13, 'add_clientdocument'),
(50, 'Can change Document Client', 13, 'change_clientdocument'),
(51, 'Can delete Document Client', 13, 'delete_clientdocument'),
(52, 'Can view Document Client', 13, 'view_clientdocument');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$hL0o03R8tZNw5O5wVtlvwz$zTtRbh44HivLGn+8ng7fcqHryH0IcBiaAHrp+sx6Jpo=', '2025-06-30 22:52:38.869768', 1, 'miage', 'AHOLIA WILFRIED CHEREL', 'ADJI', 'miage@gmail.com', 1, 1, '2025-06-26 18:01:19.000000'),
(2, 'pbkdf2_sha256$600000$HDBYLxrQS1pfwlJrhtF7ei$1/g4ixd9ezR7LETBFmg7dMVOVagna34+D8JSB6T+tEU=', '2025-07-01 06:05:53.456563', 0, 'agent', 'Jean', 'Amanie', '', 0, 1, '2025-06-27 16:48:57.000000');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(1, 2, 1);

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-06-27 16:09:57.519886', '1', 'miage', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]', 4, 1),
(2, '2025-06-27 16:48:58.278625', '2', 'agent', 1, '[{\"added\": {}}]', 4, 1),
(3, '2025-06-27 16:49:11.208343', '2', 'agent', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]', 4, 1),
(4, '2025-06-27 16:50:37.788122', '2', 'agent', 2, '[]', 4, 1),
(5, '2025-06-27 16:52:13.820799', '2', 'agent', 2, '[]', 4, 1),
(6, '2025-06-27 17:01:26.481413', '1', 'Agents', 1, '[{\"added\": {}}]', 3, 1),
(7, '2025-06-27 17:01:40.836980', '2', 'agent', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 4, 1),
(8, '2025-06-28 14:29:54.813714', '1', 'ADJI AHOLIA WILFRIED CHEREL (0546110591)', 2, '[{\"changed\": {\"fields\": [\"Lieu de naissance\", \"Adresse R\\u00e9sidentielle\", \"Fr\\u00e9quence des revenus\"]}}]', 12, 1);

-- --------------------------------------------------------

--
-- Structure de la table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(12, 'gmycom', 'client'),
(13, 'gmycom', 'clientdocument'),
(9, 'gmycom', 'compte'),
(10, 'gmycom', 'credit'),
(7, 'gmycom', 'historiquetransaction'),
(11, 'gmycom', 'mouvement'),
(8, 'gmycom', 'remboursement'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Structure de la table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-06-26 18:00:30.078055'),
(2, 'auth', '0001_initial', '2025-06-26 18:00:37.788272'),
(3, 'admin', '0001_initial', '2025-06-26 18:00:39.449719'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-06-26 18:00:39.505896'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-06-26 18:00:39.534736'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-06-26 18:00:40.092056'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-06-26 18:00:40.924027'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-06-26 18:00:41.034244'),
(9, 'auth', '0004_alter_user_username_opts', '2025-06-26 18:00:41.088130'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-06-26 18:00:41.691896'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-06-26 18:00:41.723173'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-06-26 18:00:41.767131'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-06-26 18:00:41.933100'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-06-26 18:00:42.051046'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-06-26 18:00:42.154679'),
(16, 'auth', '0011_update_proxy_permissions', '2025-06-26 18:00:42.203458'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-06-26 18:00:42.288508'),
(18, 'sessions', '0001_initial', '2025-06-26 18:00:43.087168'),
(19, 'gmycom', '0001_initial', '2025-06-27 13:54:33.691159'),
(20, 'gmycom', '0002_alter_compte_options_alter_credit_options_and_more', '2025-06-27 17:32:24.204752'),
(21, 'gmycom', '0003_alter_client_frequence_revenu_and_more', '2025-06-27 18:38:38.154533'),
(22, 'gmycom', '0004_alter_remboursement_methode_paiement', '2025-06-30 22:28:27.472651'),
(23, 'gmycom', '0005_alter_credit_compte_and_more', '2025-06-30 23:39:45.505589');

-- --------------------------------------------------------

--
-- Structure de la table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('0jo399v14z49inabnd785s8o57z1zal9', '.eJxVjDsOwjAQBe_iGlkb_01JzxmsXX9wANlSnFSIu0OkFNC-mXkvFnBba9hGXsKc2JkJdvrdCOMjtx2kO7Zb57G3dZmJ7wo_6ODXnvLzcrh_BxVH_dbKAJpYJktZogKhIeeJCoJPJmkHHo2VkkBQRKujJllULM4WAKm9cOz9AednN8E:1uWU7t:fxR41mkds6f_V5P1EIkzMiugeWBYomxcnOVI-vTdBzA', '2025-07-15 06:05:53.506923'),
('4jwcnllxg0kab67bwq4mc3w5u4t6j2ah', '.eJxVjMsOwiAQRf-FtSFCGR4u3fcbyAxDpWogKe3K-O_apAvd3nPOfYmI21ri1vMSZxYXocTpdyNMj1x3wHestyZTq-syk9wVedAux8b5eT3cv4OCvXxrYxERLPvJBDDBOFBATnNQ2evASidWCI4c2qzPhngKPhFa9DiAHwbx_gDVejet:1uWNMc:BxyEx6bQAr_eQTZvoW5blsMKFC83WyOjHVj1iBU9_50', '2025-07-14 22:52:38.895910'),
('5af1uu465e84nxgbr39okhw0pmrnqhbq', '.eJxVjMsOwiAQRf-FtSFCGR4u3fcbyAxDpWogKe3K-O_apAvd3nPOfYmI21ri1vMSZxYXocTpdyNMj1x3wHestyZTq-syk9wVedAux8b5eT3cv4OCvXxrYxERLPvJBDDBOFBATnNQ2evASidWCI4c2qzPhngKPhFa9DiAHwbx_gDVejet:1uVCHY:qPmDwQarxxiNBmkmEJ4Ecsgx6KDlqnEEMyeHe7kyyE4', '2025-07-11 16:50:32.035435'),
('5t46fpaff52i8iiewa6cvcf6i7x8hter', '.eJxVjDsOwjAQBe_iGlkb_01JzxmsXX9wANlSnFSIu0OkFNC-mXkvFnBba9hGXsKc2JkJdvrdCOMjtx2kO7Zb57G3dZmJ7wo_6ODXnvLzcrh_BxVH_dbKAJpYJktZogKhIeeJCoJPJmkHHo2VkkBQRKujJllULM4WAKm9cOz9AednN8E:1uWNXW:6NEy1Ft2n9OME_TTkncQ-LiAiFXob0lBU1FtTM4Jzc4', '2025-07-14 23:03:54.056557'),
('8vaxtatderbq2me3gmrx0pvad5nkf8be', '.eJxVjDsOwjAQBe_iGlkb_01JzxmsXX9wANlSnFSIu0OkFNC-mXkvFnBba9hGXsKc2JkJdvrdCOMjtx2kO7Zb57G3dZmJ7wo_6ODXnvLzcrh_BxVH_dbKAJpYJktZogKhIeeJCoJPJmkHHo2VkkBQRKujJllULM4WAKm9cOz9AednN8E:1uWQBH:I0o_2_n1lpQX0CVsw28oV2vfMlewHSF0Y7gbbnxHYsM', '2025-07-15 01:53:07.511149'),
('c5yg2a52qw0atrnchtysk4tzgk50yupc', '.eJxVjMsOwiAQRf-FtSFCGR4u3fcbyAxDpWogKe3K-O_apAvd3nPOfYmI21ri1vMSZxYXocTpdyNMj1x3wHestyZTq-syk9wVedAux8b5eT3cv4OCvXxrYxERLPvJBDDBOFBATnNQ2evASidWCI4c2qzPhngKPhFa9DiAHwbx_gDVejet:1uVWYC:P33XOSXffPAcL8zEetANaj7FvjbpVDftdPX1PFy68xg', '2025-07-12 14:29:04.614947'),
('ex1ggx7ozs2dq8zy8e6sfd1irls28ohu', '.eJxVjDsOwjAQBe_iGlkb_01JzxmsXX9wANlSnFSIu0OkFNC-mXkvFnBba9hGXsKc2JkJdvrdCOMjtx2kO7Zb57G3dZmJ7wo_6ODXnvLzcrh_BxVH_dbKAJpYJktZogKhIeeJCoJPJmkHHo2VkkBQRKujJllULM4WAKm9cOz9AednN8E:1uVZDY:m3aWjW6CxrGheLcpaT9jTV0ifv432s7-KoODMO3Nw8g', '2025-07-12 17:19:56.382080'),
('f522j8ij8iq690t0l1jwlwub9x1ziotz', '.eJxVjDsOwjAQBe_iGlkb_01JzxmsXX9wANlSnFSIu0OkFNC-mXkvFnBba9hGXsKc2JkJdvrdCOMjtx2kO7Zb57G3dZmJ7wo_6ODXnvLzcrh_BxVH_dbKAJpYJktZogKhIeeJCoJPJmkHHo2VkkBQRKujJllULM4WAKm9cOz9AednN8E:1uW50E:b2tiQ0GWupG5SuiwGlvmfcf7qoTBnevI4mYhynxHcrU', '2025-07-14 03:16:18.656201'),
('m1z3egp1d3yzxmzhplxb13k96ty90abn', '.eJxVjDsOwjAQBe_iGlkb_01JzxmsXX9wANlSnFSIu0OkFNC-mXkvFnBba9hGXsKc2JkJdvrdCOMjtx2kO7Zb57G3dZmJ7wo_6ODXnvLzcrh_BxVH_dbKAJpYJktZogKhIeeJCoJPJmkHHo2VkkBQRKujJllULM4WAKm9cOz9AednN8E:1uWNLY:UMzkzmKSjNH8YGh7RBklpNsVS_6X5GK_0baO45aj8Wc', '2025-07-14 22:51:32.767951'),
('r6mp1bljws1m0zhdmy24pvqpwhjyyh8l', '.eJxVjDsOwjAQBe_iGlkb_01JzxmsXX9wANlSnFSIu0OkFNC-mXkvFnBba9hGXsKc2JkJdvrdCOMjtx2kO7Zb57G3dZmJ7wo_6ODXnvLzcrh_BxVH_dbKAJpYJktZogKhIeeJCoJPJmkHHo2VkkBQRKujJllULM4WAKm9cOz9AednN8E:1uVv7B:KLYWIetqg_SuGzQsZ1L5nVaDGRTEZAFg4U3zGIjhvEA', '2025-07-13 16:42:49.905912'),
('selfzxaalec5z8urmkli7ks325679hpi', '.eJxVjMsOwiAQRf-FtSFCGR4u3fcbyAxDpWogKe3K-O_apAvd3nPOfYmI21ri1vMSZxYXocTpdyNMj1x3wHestyZTq-syk9wVedAux8b5eT3cv4OCvXxrYxERLPvJBDDBOFBATnNQ2evASidWCI4c2qzPhngKPhFa9DiAHwbx_gDVejet:1uWL52:wUxe1p2mAqfgkYz0nIOwZVx-aRVFmLq1cXbNlPkTMjI', '2025-07-14 20:26:20.887621'),
('t4yfnpz7gyegv9s8z6sxaougttrg92xu', '.eJxVjMsOwiAQRf-FtSFCGR4u3fcbyAxDpWogKe3K-O_apAvd3nPOfYmI21ri1vMSZxYXocTpdyNMj1x3wHestyZTq-syk9wVedAux8b5eT3cv4OCvXxrYxERLPvJBDDBOFBATnNQ2evASidWCI4c2qzPhngKPhFa9DiAHwbx_gDVejet:1uVZAO:S086ScCMFHnwTc3M3oSladzMW-YPFgfUMnYBcetsD1o', '2025-07-12 17:16:40.525391'),
('uaar3vk2tynbwtnzb4o5yrkj364hbu1d', '.eJxVjMsOwiAQRf-FtSFCGR4u3fcbyAxDpWogKe3K-O_apAvd3nPOfYmI21ri1vMSZxYXocTpdyNMj1x3wHestyZTq-syk9wVedAux8b5eT3cv4OCvXxrYxERLPvJBDDBOFBATnNQ2evASidWCI4c2qzPhngKPhFa9DiAHwbx_gDVejet:1uWM3r:NJogOZw4YiT1Y-SesFUEdu7Q5mnmsXv6kh-Zi5Gp-GE', '2025-07-14 21:29:11.304046'),
('y28bqukzzo115j4qq6n31wt5fcstn7gr', '.eJxVjDsOwjAQBe_iGlkb_01JzxmsXX9wANlSnFSIu0OkFNC-mXkvFnBba9hGXsKc2JkJdvrdCOMjtx2kO7Zb57G3dZmJ7wo_6ODXnvLzcrh_BxVH_dbKAJpYJktZogKhIeeJCoJPJmkHHo2VkkBQRKujJllULM4WAKm9cOz9AednN8E:1uW59d:nh5YfWHVnyKCkFy-B4e-CFvrOB6ZJ1X6pLPitcpbCWU', '2025-07-14 03:26:01.732786');

-- --------------------------------------------------------

--
-- Structure de la table `gmycom_client`
--

CREATE TABLE `gmycom_client` (
  `id` bigint(20) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `telephone` varchar(20) NOT NULL,
  `adresse` longtext NOT NULL,
  `profession` varchar(100) DEFAULT NULL,
  `revenu_mensuel` decimal(10,2) DEFAULT NULL,
  `situation_matrimoniale` varchar(1) DEFAULT NULL,
  `agent_id` int(11) DEFAULT NULL,
  `adresse_pays` varchar(100) DEFAULT NULL,
  `anciennete_emploi` int(10) UNSIGNED DEFAULT NULL CHECK (`anciennete_emploi` >= 0),
  `date_creation` datetime(6) NOT NULL,
  `date_modification` datetime(6) NOT NULL,
  `date_naissance` date DEFAULT NULL,
  `frequence_revenu` varchar(50) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `lieu_naissance` varchar(100) DEFAULT NULL,
  `nationalite` varchar(100) NOT NULL,
  `nom_employeur` varchar(255) DEFAULT NULL,
  `nombre_personnes_charge` int(10) UNSIGNED DEFAULT NULL CHECK (`nombre_personnes_charge` >= 0),
  `secteur_activite` varchar(100) DEFAULT NULL,
  `sexe` varchar(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `gmycom_client`
--

INSERT INTO `gmycom_client` (`id`, `nom`, `prenom`, `email`, `telephone`, `adresse`, `profession`, `revenu_mensuel`, `situation_matrimoniale`, `agent_id`, `adresse_pays`, `anciennete_emploi`, `date_creation`, `date_modification`, `date_naissance`, `frequence_revenu`, `is_active`, `lieu_naissance`, `nationalite`, `nom_employeur`, `nombre_personnes_charge`, `secteur_activite`, `sexe`) VALUES
(2, 'KOUMA', 'WILLY', 'kouma@example.com', '0104352060', 'Abobo baoulé', 'Commerçant(e)', 200000.00, 'C', 2, 'Côte d\'Ivoire', 12, '2025-06-28 11:32:52.550149', '2025-06-28 11:32:52.550149', '1984-07-20', 'MENSUEL', 1, 'SOUBRE', 'Ivoirienne', 'SOCOCE', 0, 'Commerce Gros&Détail', 'M'),
(6, 'KOUADIO', 'PIERRE', 'pierre@example.com', '0777082035', 'Cocody', 'Étudiant(e)', 50000.00, 'C', 2, 'Côte d\'Ivoire', NULL, '2025-06-28 12:04:47.739897', '2025-06-28 12:04:47.739897', '1994-02-20', 'MENSUEL', 1, 'BOUAKE', 'Ivoirienne', NULL, 0, 'Administration des Affaires', 'M'),
(7, 'ASSI', 'JEAN', 'assi@example.com', '0103770737', 'Bingerville,Abatta', 'Médecin', 800000.00, 'M', 2, 'Côte d\'Ivoire', 120, '2025-06-29 01:55:02.642626', '2025-06-29 01:55:02.642626', '1983-07-11', 'MENSUEL', 1, 'SINFRA', 'Ivoirienne', 'CHU Cocody', 3, 'Médecine', 'M'),
(8, 'ASSI', 'PIERRE', 'assie@example.com', '0103770736', 'Ahouabo', 'Retraité(e)', 300000.00, 'D', 2, 'Côte d\'Ivoire', NULL, '2025-06-29 02:50:40.842054', '2025-06-29 02:50:40.842054', '1980-01-11', 'BIMENSUEL', 1, 'SOUBRE', 'Ivoirienne', 'SOCOCE', 0, 'Administration des Affaires', 'M'),
(9, 'DABILA', 'GRÂCE', 'dabila@example.com', '0104352066', 'Agboville', 'Comptable', 400000.00, 'C', 2, 'Côte d\'Ivoire', NULL, '2025-06-29 06:07:52.014274', '2025-06-29 06:07:52.014274', '1985-05-24', 'MENSUEL', 1, 'TREICHVILLE', 'Ivoirienne', 'NSIA Banque', 0, 'Finance', 'M'),
(10, 'KONE', 'ABOUDRAMANE', 'kone@example.com', '0778082035', 'AZAGUIE', 'Planteur', 400000.00, 'C', 2, 'Côte d\'Ivoire', NULL, '2025-06-29 06:14:18.150844', '2025-06-29 06:14:18.150844', '1998-04-30', 'BIMENSUEL', 1, 'ADJAME', 'Ivoirienne', 'Coopérative Eco', 5, 'Agriculture', 'M');

-- --------------------------------------------------------

--
-- Structure de la table `gmycom_clientdocument`
--

CREATE TABLE `gmycom_clientdocument` (
  `id` bigint(20) NOT NULL,
  `type_document` varchar(20) NOT NULL,
  `fichier` varchar(100) NOT NULL,
  `date_telechargement` datetime(6) NOT NULL,
  `description` longtext DEFAULT NULL,
  `client_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `gmycom_clientdocument`
--

INSERT INTO `gmycom_clientdocument` (`id`, `type_document`, `fichier`, `date_telechargement`, `description`, `client_id`) VALUES
(3, 'PHOTO_ID', 'client_docs/2/others/20241107085048284.jpg', '2025-06-28 11:32:52.844158', '', 2),
(4, 'CIN_RECTO', 'client_docs/2/others/IMG_20230112_1146292.jpg', '2025-06-28 11:32:52.873389', '', 2),
(5, 'JUST_DOM', 'client_docs/2/others/monCV.pdf', '2025-06-28 11:32:53.005386', '', 2),
(16, 'CIN_RECTO', 'client_docs/6/others/IMG_20230112_1146292.jpg', '2025-06-28 12:04:47.882371', '', 6),
(17, 'JUST_DOM', 'client_docs/6/others/IMG_20250622_165915_366.jpg', '2025-06-28 12:04:47.885369', '', 6),
(18, 'PHOTO_ID', 'client_docs/6/others/3ac36be0e27a27c33b3fa287a3b3b174.jpg', '2025-06-28 12:04:47.940849', '', 6),
(19, 'PHOTO_ID', 'client_docs/7/others/1000027555_1fc849e0c0180b8e1373a76094a15f81-26_06_2023_02_46_35.jpg', '2025-06-29 01:55:02.700771', '', 7),
(20, 'CIN_RECTO', 'client_docs/7/others/122159578_433.png', '2025-06-29 01:55:02.731217', '', 7),
(21, 'JUST_DOM', 'client_docs/7/others/listeDePresenceCEPS.docx', '2025-06-29 01:55:02.735291', '', 7),
(22, 'CIN_RECTO', 'client_docs/8/others/9.png', '2025-06-29 02:50:40.887687', '', 8),
(23, 'PHOTO_ID', 'client_docs/8/others/1000027555_1fc849e0c0180b8e1373a76094a15f81-26_06_2023_02_46_35.jpg', '2025-06-29 02:50:40.887687', '', 8),
(24, 'JUST_DOM', 'client_docs/8/others/programCom.pdf', '2025-06-29 02:50:40.897697', '', 8),
(25, 'CIN_RECTO', 'client_docs/9/others/13.jpeg', '2025-06-29 06:07:52.050341', '', 9),
(26, 'JUST_DOM', 'client_docs/9/others/12.jpeg', '2025-06-29 06:07:52.050341', '', 9),
(27, 'PHOTO_ID', 'client_docs/9/others/3.jpg', '2025-06-29 06:07:52.050341', '', 9),
(28, 'CIN_RECTO', 'client_docs/10/others/aide.jpeg', '2025-06-29 06:14:18.308651', '', 10),
(29, 'JUST_DOM', 'client_docs/10/others/monCV.pdf', '2025-06-29 06:14:18.488660', '', 10),
(30, 'PHOTO_ID', 'client_docs/10/others/thoughtful-afro-student-thinking-online-management-project.jpg', '2025-06-29 06:14:18.519832', '', 10);

-- --------------------------------------------------------

--
-- Structure de la table `gmycom_compte`
--

CREATE TABLE `gmycom_compte` (
  `id` bigint(20) NOT NULL,
  `type_compte` varchar(10) NOT NULL,
  `solde` decimal(15,2) NOT NULL,
  `numero_compte` varchar(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `client_id` bigint(20) NOT NULL,
  `opened_by_id` int(11) DEFAULT NULL,
  `date_ouverture` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `gmycom_compte`
--

INSERT INTO `gmycom_compte` (`id`, `type_compte`, `solde`, `numero_compte`, `is_active`, `client_id`, `opened_by_id`, `date_ouverture`) VALUES
(2, 'epargne', 0.00, 'COMPTE-441A7064', 1, 2, 2, '2025-06-28 11:32:52.581405'),
(7, 'courant', 10000.00, 'COMPTE-B9DCB484', 1, 2, 2, '2025-06-29 01:44:21.014778'),
(9, 'epargne', 0.00, 'COMPTE-16A31135', 1, 7, 2, '2025-06-29 01:55:02.658340'),
(10, 'epargne', 0.00, 'COMPTE-9F200779', 1, 8, 2, '2025-06-29 02:50:40.887687'),
(11, 'epargne', 25000.00, 'COMPTE-8BD88754', 1, 9, 2, '2025-06-29 06:07:52.034716'),
(12, 'epargne', 37000.00, 'COMPTE-A5CBFB3F', 1, 10, 2, '2025-06-29 06:14:18.228963');

-- --------------------------------------------------------

--
-- Structure de la table `gmycom_credit`
--

CREATE TABLE `gmycom_credit` (
  `id` bigint(20) NOT NULL,
  `numero_credit` varchar(20) NOT NULL,
  `amount_granted` decimal(15,2) NOT NULL,
  `interest_rate` decimal(5,2) NOT NULL,
  `duree_mois` int(10) UNSIGNED NOT NULL CHECK (`duree_mois` >= 0),
  `due_date` date NOT NULL,
  `total_interest_expected` decimal(15,2) NOT NULL,
  `total_expected_repayment` decimal(15,2) NOT NULL,
  `amount_repaid` decimal(15,2) NOT NULL,
  `status` varchar(10) NOT NULL,
  `client_id` bigint(20) NOT NULL,
  `compte_id` bigint(20) DEFAULT NULL,
  `granted_by_id` int(11) DEFAULT NULL,
  `date_demande` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `gmycom_credit`
--

INSERT INTO `gmycom_credit` (`id`, `numero_credit`, `amount_granted`, `interest_rate`, `duree_mois`, `due_date`, `total_interest_expected`, `total_expected_repayment`, `amount_repaid`, `status`, `client_id`, `compte_id`, `granted_by_id`, `date_demande`) VALUES
(1, 'CREDIT-385E5A6E', 0.05, 222.00, 2222, '2210-08-30', 20.55, 20.60, 0.00, 'REJECTED', 10, 12, 2, '2025-06-30 05:21:44.666367'),
(2, 'CREDIT-F3E5D077', 75000.00, 14.00, 23, '2027-05-30', 20125.00, 95125.00, 24500.00, 'ACTIVE', 9, 11, 1, '2025-06-30 05:26:27.769572'),
(3, 'CREDIT-F0DE6977', 75000.00, 14.00, 23, '2027-05-30', 20125.00, 95125.00, 0.00, 'REJECTED', 9, 11, 1, '2025-06-30 05:28:49.951823'),
(4, 'CREDIT-C88D69E9', 50000.00, 9.00, 12, '2026-07-01', 2470.84, 52470.84, 0.00, 'PENDING', 10, 12, 2, '2025-07-01 00:46:07.009297'),
(5, 'CREDIT-58DFC9F2', 50000.00, 9.00, 12, '2026-07-01', 2470.84, 52470.84, 0.00, 'PENDING', 10, 12, 2, '2025-07-01 00:47:33.571630'),
(6, 'CREDIT-F221AD08', 50000.00, 9.00, 12, '2026-07-01', 2470.84, 52470.84, 13000.00, 'ACTIVE', 10, 12, 2, '2025-07-01 00:49:38.278447');

-- --------------------------------------------------------

--
-- Structure de la table `gmycom_historiquetransaction`
--

CREATE TABLE `gmycom_historiquetransaction` (
  `id` bigint(20) NOT NULL,
  `type_operation` varchar(20) NOT NULL,
  `montant` decimal(15,2) NOT NULL,
  `date_operation` datetime(6) NOT NULL,
  `description` longtext DEFAULT NULL,
  `compte_id` bigint(20) DEFAULT NULL,
  `credit_id` bigint(20) DEFAULT NULL,
  `mouvement_id` bigint(20) DEFAULT NULL,
  `remboursement_id` bigint(20) DEFAULT NULL,
  `agent_id` int(11) DEFAULT NULL,
  `solde_apres` decimal(15,2) DEFAULT NULL,
  `solde_avant` decimal(15,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `gmycom_historiquetransaction`
--

INSERT INTO `gmycom_historiquetransaction` (`id`, `type_operation`, `montant`, `date_operation`, `description`, `compte_id`, `credit_id`, `mouvement_id`, `remboursement_id`, `agent_id`, `solde_apres`, `solde_avant`) VALUES
(1, 'DEPOT', 100000.00, '2025-06-29 18:30:10.328284', '', 11, NULL, NULL, NULL, 2, 100000.00, 0.00),
(2, 'RETRAIT', 75000.00, '2025-06-30 05:26:28.027587', 'Décaissement crédit CREDIT-F3E5D077', 11, NULL, NULL, NULL, 1, 25000.00, 100000.00),
(3, 'CREDIT', 75000.00, '2025-06-30 05:26:28.107132', 'Décaissement du crédit CREDIT-F3E5D077', 11, 2, NULL, NULL, 1, 25000.00, 100000.00),
(4, 'REMBOURSEMENT', 24500.00, '2025-06-30 23:04:33.557922', 'Remboursement de 24500 pour crédit CREDIT-F3E5D077', 11, 2, NULL, 1, 2, NULL, NULL),
(5, 'DEPOT', 100000.00, '2025-07-01 00:45:23.190848', '', 12, NULL, NULL, NULL, 2, 100000.00, 0.00),
(8, 'DEPOT', 50000.00, '2025-07-01 00:49:38.605371', 'Décaissement crédit CREDIT-F221AD08', 12, NULL, NULL, NULL, 2, 150000.00, 100000.00),
(9, 'DECAISSEMENT_CREDIT', 50000.00, '2025-07-01 00:49:38.606385', 'Décaissement du crédit CREDIT-F221AD08 vers client KONE ABOUDRAMANE', 12, 6, NULL, NULL, 2, 150000.00, 100000.00),
(14, 'RETRAIT', 13000.00, '2025-07-01 03:59:44.609420', 'Remboursement crédit CREDIT-F221AD08', 12, NULL, NULL, NULL, 2, 137000.00, 150000.00),
(15, 'REMBOURSEMENT', 13000.00, '2025-07-01 03:59:44.692396', 'Remboursement de 13000 XOF pour crédit CREDIT-F221AD08 par KONE ABOUDRAMANE', 12, 6, NULL, 6, 2, 137000.00, 150000.00),
(16, 'RETRAIT', 100000.00, '2025-07-01 06:04:20.392497', '', 12, NULL, NULL, NULL, 2, 37000.00, 137000.00);

-- --------------------------------------------------------

--
-- Structure de la table `gmycom_mouvement`
--

CREATE TABLE `gmycom_mouvement` (
  `id` bigint(20) NOT NULL,
  `type_mouvement` varchar(10) NOT NULL,
  `montant` decimal(15,2) NOT NULL,
  `date_mouvement` datetime(6) NOT NULL,
  `description` longtext DEFAULT NULL,
  `agent_id` int(11) DEFAULT NULL,
  `compte_id` bigint(20) NOT NULL,
  `compte_destinataire_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `gmycom_mouvement`
--

INSERT INTO `gmycom_mouvement` (`id`, `type_mouvement`, `montant`, `date_mouvement`, `description`, `agent_id`, `compte_id`, `compte_destinataire_id`) VALUES
(1, 'DEPOT', 100000.00, '2025-06-29 18:30:10.362684', '', 2, 11, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `gmycom_remboursement`
--

CREATE TABLE `gmycom_remboursement` (
  `id` bigint(20) NOT NULL,
  `numero_remboursement` varchar(20) NOT NULL,
  `montant` decimal(15,2) NOT NULL,
  `date_remboursement` datetime(6) NOT NULL,
  `methode_paiement` varchar(50) NOT NULL,
  `reference` varchar(100) DEFAULT NULL,
  `notes` longtext DEFAULT NULL,
  `agent_id` int(11) DEFAULT NULL,
  `credit_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `gmycom_remboursement`
--

INSERT INTO `gmycom_remboursement` (`id`, `numero_remboursement`, `montant`, `date_remboursement`, `methode_paiement`, `reference`, `notes`, `agent_id`, `credit_id`) VALUES
(1, 'RMB-FF7343C6', 24500.00, '2025-06-30 23:04:33.530935', 'CASH', NULL, '', 2, 2),
(6, 'RMB-A111555F', 13000.00, '2025-07-01 03:59:44.611453', 'MOBILE_MONEY', 'REF-01', '', 2, 6);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Index pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Index pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Index pour la table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Index pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Index pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Index pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Index pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Index pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Index pour la table `gmycom_client`
--
ALTER TABLE `gmycom_client`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `telephone` (`telephone`),
  ADD UNIQUE KEY `gmycom_client_email_8aa6010d_uniq` (`email`),
  ADD KEY `gmycom_client_agent_id_772fd2ab_fk_auth_user_id` (`agent_id`);

--
-- Index pour la table `gmycom_clientdocument`
--
ALTER TABLE `gmycom_clientdocument`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `gmycom_clientdocument_client_id_type_document_c6a320d7_uniq` (`client_id`,`type_document`);

--
-- Index pour la table `gmycom_compte`
--
ALTER TABLE `gmycom_compte`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_compte` (`numero_compte`),
  ADD KEY `gmycom_compte_opened_by_id_bd7a81d4_fk_auth_user_id` (`opened_by_id`),
  ADD KEY `gmycom_compte_client_id_d61a35e8` (`client_id`);

--
-- Index pour la table `gmycom_credit`
--
ALTER TABLE `gmycom_credit`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_credit` (`numero_credit`),
  ADD KEY `gmycom_credit_client_id_975c7db7_fk_gmycom_client_id` (`client_id`),
  ADD KEY `gmycom_credit_granted_by_id_e0abcbea_fk_auth_user_id` (`granted_by_id`),
  ADD KEY `gmycom_credit_compte_id_fc9a0b0d_fk_gmycom_compte_id` (`compte_id`);

--
-- Index pour la table `gmycom_historiquetransaction`
--
ALTER TABLE `gmycom_historiquetransaction`
  ADD PRIMARY KEY (`id`),
  ADD KEY `gmycom_historiquetra_credit_id_5dd71500_fk_gmycom_cr` (`credit_id`),
  ADD KEY `gmycom_historiquetra_mouvement_id_f9fe296e_fk_gmycom_mo` (`mouvement_id`),
  ADD KEY `gmycom_historiquetra_remboursement_id_3388fcc5_fk_gmycom_re` (`remboursement_id`),
  ADD KEY `gmycom_historiquetransaction_agent_id_98e410eb_fk_auth_user_id` (`agent_id`),
  ADD KEY `gmycom_historiquetra_compte_id_38b4daa9_fk_gmycom_co` (`compte_id`);

--
-- Index pour la table `gmycom_mouvement`
--
ALTER TABLE `gmycom_mouvement`
  ADD PRIMARY KEY (`id`),
  ADD KEY `gmycom_mouvement_agent_id_48f6b3ff_fk_auth_user_id` (`agent_id`),
  ADD KEY `gmycom_mouvement_compte_id_5c46a069_fk_gmycom_compte_id` (`compte_id`),
  ADD KEY `gmycom_mouvement_compte_destinataire__33714515_fk_gmycom_co` (`compte_destinataire_id`);

--
-- Index pour la table `gmycom_remboursement`
--
ALTER TABLE `gmycom_remboursement`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_remboursement` (`numero_remboursement`),
  ADD KEY `gmycom_remboursement_agent_id_3047829a_fk_auth_user_id` (`agent_id`),
  ADD KEY `gmycom_remboursement_credit_id_bd39798a_fk_gmycom_credit_id` (`credit_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT pour la table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT pour la table `gmycom_client`
--
ALTER TABLE `gmycom_client`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT pour la table `gmycom_clientdocument`
--
ALTER TABLE `gmycom_clientdocument`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT pour la table `gmycom_compte`
--
ALTER TABLE `gmycom_compte`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT pour la table `gmycom_credit`
--
ALTER TABLE `gmycom_credit`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT pour la table `gmycom_historiquetransaction`
--
ALTER TABLE `gmycom_historiquetransaction`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT pour la table `gmycom_mouvement`
--
ALTER TABLE `gmycom_mouvement`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `gmycom_remboursement`
--
ALTER TABLE `gmycom_remboursement`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Contraintes pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Contraintes pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `gmycom_client`
--
ALTER TABLE `gmycom_client`
  ADD CONSTRAINT `gmycom_client_agent_id_772fd2ab_fk_auth_user_id` FOREIGN KEY (`agent_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `gmycom_clientdocument`
--
ALTER TABLE `gmycom_clientdocument`
  ADD CONSTRAINT `gmycom_clientdocument_client_id_fe204301_fk_gmycom_client_id` FOREIGN KEY (`client_id`) REFERENCES `gmycom_client` (`id`);

--
-- Contraintes pour la table `gmycom_compte`
--
ALTER TABLE `gmycom_compte`
  ADD CONSTRAINT `gmycom_compte_client_id_d61a35e8_fk_gmycom_client_id` FOREIGN KEY (`client_id`) REFERENCES `gmycom_client` (`id`),
  ADD CONSTRAINT `gmycom_compte_opened_by_id_bd7a81d4_fk_auth_user_id` FOREIGN KEY (`opened_by_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `gmycom_credit`
--
ALTER TABLE `gmycom_credit`
  ADD CONSTRAINT `gmycom_credit_client_id_975c7db7_fk_gmycom_client_id` FOREIGN KEY (`client_id`) REFERENCES `gmycom_client` (`id`),
  ADD CONSTRAINT `gmycom_credit_compte_id_fc9a0b0d_fk_gmycom_compte_id` FOREIGN KEY (`compte_id`) REFERENCES `gmycom_compte` (`id`),
  ADD CONSTRAINT `gmycom_credit_granted_by_id_e0abcbea_fk_auth_user_id` FOREIGN KEY (`granted_by_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `gmycom_historiquetransaction`
--
ALTER TABLE `gmycom_historiquetransaction`
  ADD CONSTRAINT `gmycom_historiquetra_compte_id_38b4daa9_fk_gmycom_co` FOREIGN KEY (`compte_id`) REFERENCES `gmycom_compte` (`id`),
  ADD CONSTRAINT `gmycom_historiquetra_credit_id_5dd71500_fk_gmycom_cr` FOREIGN KEY (`credit_id`) REFERENCES `gmycom_credit` (`id`),
  ADD CONSTRAINT `gmycom_historiquetra_mouvement_id_f9fe296e_fk_gmycom_mo` FOREIGN KEY (`mouvement_id`) REFERENCES `gmycom_mouvement` (`id`),
  ADD CONSTRAINT `gmycom_historiquetra_remboursement_id_3388fcc5_fk_gmycom_re` FOREIGN KEY (`remboursement_id`) REFERENCES `gmycom_remboursement` (`id`),
  ADD CONSTRAINT `gmycom_historiquetransaction_agent_id_98e410eb_fk_auth_user_id` FOREIGN KEY (`agent_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `gmycom_mouvement`
--
ALTER TABLE `gmycom_mouvement`
  ADD CONSTRAINT `gmycom_mouvement_agent_id_48f6b3ff_fk_auth_user_id` FOREIGN KEY (`agent_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `gmycom_mouvement_compte_destinataire__33714515_fk_gmycom_co` FOREIGN KEY (`compte_destinataire_id`) REFERENCES `gmycom_compte` (`id`),
  ADD CONSTRAINT `gmycom_mouvement_compte_id_5c46a069_fk_gmycom_compte_id` FOREIGN KEY (`compte_id`) REFERENCES `gmycom_compte` (`id`);

--
-- Contraintes pour la table `gmycom_remboursement`
--
ALTER TABLE `gmycom_remboursement`
  ADD CONSTRAINT `gmycom_remboursement_agent_id_3047829a_fk_auth_user_id` FOREIGN KEY (`agent_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `gmycom_remboursement_credit_id_bd39798a_fk_gmycom_credit_id` FOREIGN KEY (`credit_id`) REFERENCES `gmycom_credit` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
