-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost
-- Généré le : mer. 24 juin 2026 à 19:03
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `base_pedagogique`
--

-- --------------------------------------------------------

--
-- Structure de la table `accounts_users`
--

CREATE TABLE `accounts_users` (
  `id` int(11) NOT NULL,
  `username` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(128) NOT NULL,
  `role` enum('ELEVE','ENSEIGNANT') NOT NULL,
  `date_joined` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `accounts_users`
--

INSERT INTO `accounts_users` (`id`, `username`, `email`, `password`, `role`, `date_joined`) VALUES
(1, 'M. KALOA', 'kaloaabdoul@gmail.com', '00344', 'ENSEIGNANT', '2026-06-24 15:34:32'),
(2, 'Ali', 'kibaoali@gmail.com', '000000', 'ELEVE', '2026-06-24 15:34:32'),
(3, 'Miere', 'aloor@gmail.com', '00000', 'ENSEIGNANT', '2026-06-24 15:34:32'),
(4, 'Heren', 'renne@gmail.com', '1000', 'ELEVE', '2026-06-24 15:34:32'),
(5, 'Mme FATIMA', 'Fatima44@gmail.com', '05', 'ENSEIGNANT', '2026-06-24 15:34:32'),
(6, 'Mme KALI', 'oreliecm@gmail.com', '06', 'ENSEIGNANT', '2026-06-24 15:34:32'),
(7, 'Mme Mireille', 'mireille20045@gmail.com', '07', 'ENSEIGNANT', '2026-06-24 15:34:32'),
(8, 'M. PITOLO Seth', 'sethpitolo@gmail.com', '08', 'ENSEIGNANT', '2026-06-24 15:34:32'),
(9, 'Nara', 'nara02009@gmail.com', '09', 'ELEVE', '2026-06-24 15:34:32'),
(10, 'M. PALLA', 'pallaseth@gmail.com', '10', 'ENSEIGNANT', '2026-06-24 15:34:32');

-- --------------------------------------------------------

--
-- Structure de la table `categories_matiere`
--

CREATE TABLE `categories_matiere` (
  `id` int(11) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `code` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `categories_matiere`
--

INSERT INTO `categories_matiere` (`id`, `nom`, `code`) VALUES
(1, 'Français', ''),
(2, 'Anglais', 'ANG'),
(3, 'Mathématiques', 'Maths'),
(4, 'Sciences de la vie et de la terre', 'SVT'),
(5, 'Allemand', 'ALL'),
(6, 'Physique-chimie', 'PC'),
(7, 'Histoire-géographie', 'H-G'),
(8, 'Enseignement Menager', 'EM'),
(9, 'Sport', 'EPS'),
(10, 'Philosophie', 'PHILO'),
(11, 'Français', 'FR'),
(12, 'Physique', NULL),
(13, 'Espagnol', NULL),
(14, 'Chimie', NULL);

-- --------------------------------------------------------

--
-- Structure de la table `categories_niveau`
--

CREATE TABLE `categories_niveau` (
  `id` int(11) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `sigle` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `categories_niveau`
--

INSERT INTO `categories_niveau` (`id`, `nom`, `sigle`) VALUES
(1, 'Seconde', NULL),
(2, 'Troisième', NULL),
(3, 'Terminale', 'Tle'),
(4, 'Troisième', '3 ème'),
(5, 'Première', '1 ère'),
(6, 'Sixième', '6 ème'),
(7, 'Ciquième', '5 ème');

-- --------------------------------------------------------

--
-- Structure de la table `ratings_commentaire`
--

CREATE TABLE `ratings_commentaire` (
  `id` int(11) NOT NULL,
  `contenu` text NOT NULL,
  `date_publication` datetime NOT NULL DEFAULT current_timestamp(),
  `id_user` int(11) NOT NULL,
  `id_doc` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `ratings_commentaire`
--

INSERT INTO `ratings_commentaire` (`id`, `contenu`, `date_publication`, `id_user`, `id_doc`) VALUES
(1, 'je trouve ce cours interesant', '2026-06-24 16:23:07', 2, 4),
(2, 'J\'ai du mal à comprendre', '2026-06-24 16:23:07', 4, 4),
(3, 'Phyique est un cours bizarre', '2026-06-24 16:23:07', 3, 3),
(4, 'J\'aime beaucoup l\'allemand', '2026-06-24 16:23:07', 9, 4),
(5, 'ce cours est tres comprehensible', '2026-06-24 16:23:07', 9, 2);

-- --------------------------------------------------------

--
-- Structure de la table `resources_documents`
--

CREATE TABLE `resources_documents` (
  `id` int(11) NOT NULL,
  `titre` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `fichier` varchar(100) NOT NULL,
  `date_publication` datetime NOT NULL DEFAULT current_timestamp(),
  `id_user` int(11) NOT NULL,
  `id_niveau` int(11) NOT NULL,
  `id_matiere` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `resources_documents`
--

INSERT INTO `resources_documents` (`id`, `titre`, `description`, `fichier`, `date_publication`, `id_user`, `id_niveau`, `id_matiere`) VALUES
(1, 'cours d\'anglais', 'ce cours est un cours de grammaire e la classe de Terminale', '', '2026-06-24 16:16:47', 5, 3, 2),
(2, 'Cours de FR', 'cours de Seconde ', '', '2026-06-24 16:16:47', 5, 1, 11),
(3, 'cours de physique', 'cours sur l\'energie cinétique', '', '2026-06-24 16:16:47', 8, 3, 12),
(4, 'cours d\'Allemand', '', '', '2026-06-24 16:16:47', 10, 3, 5),
(5, 'cours d\'HG', 'Histoire et géographie', '', '2026-06-24 16:16:47', 7, 1, 7);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `accounts_users`
--
ALTER TABLE `accounts_users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Index pour la table `categories_matiere`
--
ALTER TABLE `categories_matiere`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`code`);

--
-- Index pour la table `categories_niveau`
--
ALTER TABLE `categories_niveau`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `ratings_commentaire`
--
ALTER TABLE `ratings_commentaire`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_comm_user_unique` (`id_user`),
  ADD KEY `fk_comm_res_unique` (`id_doc`);

--
-- Index pour la table `resources_documents`
--
ALTER TABLE `resources_documents`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_res_auteur_unique` (`id_user`),
  ADD KEY `fk_res_niveau_unique` (`id_niveau`),
  ADD KEY `fk_res_matiere_unique` (`id_matiere`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `accounts_users`
--
ALTER TABLE `accounts_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT pour la table `categories_matiere`
--
ALTER TABLE `categories_matiere`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT pour la table `categories_niveau`
--
ALTER TABLE `categories_niveau`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT pour la table `ratings_commentaire`
--
ALTER TABLE `ratings_commentaire`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `resources_documents`
--
ALTER TABLE `resources_documents`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `ratings_commentaire`
--
ALTER TABLE `ratings_commentaire`
  ADD CONSTRAINT `fk_comm_res_unique` FOREIGN KEY (`id_doc`) REFERENCES `resources_documents` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_comm_user_unique` FOREIGN KEY (`id_user`) REFERENCES `accounts_users` (`id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `resources_documents`
--
ALTER TABLE `resources_documents`
  ADD CONSTRAINT `fk_res_auteur_unique` FOREIGN KEY (`id_user`) REFERENCES `accounts_users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_res_matiere_unique` FOREIGN KEY (`id_matiere`) REFERENCES `categories_matiere` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_res_niveau_unique` FOREIGN KEY (`id_niveau`) REFERENCES `categories_niveau` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
