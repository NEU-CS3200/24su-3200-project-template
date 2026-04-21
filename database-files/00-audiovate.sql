DROP DATABASE IF EXISTS Audiovate;
CREATE DATABASE IF NOT EXISTS Audiovate;
USE Audiovate;

CREATE TABLE user (
  user_id           INT AUTO_INCREMENT PRIMARY KEY,
  first_name        VARCHAR(50),
  last_name         VARCHAR(50),
  role              ENUM('User', 'Admin', 'Label Head', 'Data Analyst') DEFAULT 'User',
  email             VARCHAR(75) Unique
);

CREATE TABLE location (
    location_id      INT AUTO_INCREMENT PRIMARY KEY,
    country          VARCHAR(75) NOT NULL,
    region_state     VARCHAR(75) NOT NULL,
    city             VARCHAR(75) NOT NULL,
    postal_code      INT,
    longitude        INT,
    latitude         INT
);

CREATE TABLE platform (
    platform_id      INT AUTO_INCREMENT PRIMARY KEY,
    name             VARCHAR(50) NOT NULL,
    estim_rev_per_unit DECIMAL(11,2)
);

CREATE TABLE artist (
    artist_id      INT AUTO_INCREMENT PRIMARY KEY,
    stage_name     VARCHAR(50),
    bio            TEXT,
    instagram      VARCHAR(100),
    profile_pic    VARCHAR(225),
    tax_id_status  TINYINT(1),
    artist_user_id INT NOT NULL,
    CONSTRAINT fk_artist_user_id
    FOREIGN KEY (artist_user_id) REFERENCES user(user_id)
    ON DELETE CASCADE
);

CREATE TABLE systemLog (
    log_id          INT AUTO_INCREMENT PRIMARY KEY,
    status          TINYINT(1),
    description     TEXT,
    timestamp       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    log_user_id     INT NOT NULL,
    log_admin_id    INT NOT NULL,
    CONSTRAINT fk_log_user_id
    FOREIGN KEY (log_user_id) REFERENCES user(user_id)
    ON DELETE CASCADE,
    CONSTRAINT fk_log_admin_id
    FOREIGN KEY (log_admin_id) REFERENCES user(user_id)
    ON DELETE CASCADE
);

CREATE TABLE helpRequest (
    request_id      INT AUTO_INCREMENT PRIMARY KEY,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    submitted_user_id  INT NOT NULL,
    status             TINYINT(1),
    description        TEXT,
    assigned_admin_id   INT NOT NULL,
    CONSTRAINT fk_submitted_user_id
    FOREIGN KEY (submitted_user_id) REFERENCES user(user_id),
    CONSTRAINT fk_assigned_admin_id
    FOREIGN KEY (assigned_admin_id) REFERENCES user(user_id)
);

CREATE TABLE listener (
    listener_id       INT AUTO_INCREMENT PRIMARY KEY,
    age               INT,
    gender            ENUM('F','M','NB','Other'),
    listener_location_id INT NOT NULL,
    CONSTRAINT fk_listener_location_id
    FOREIGN KEY (listener_location_id) REFERENCES location(location_id)
);

CREATE TABLE playlist (
    playlist_id       INT AUTO_INCREMENT PRIMARY KEY,
    name              VARCHAR(50) NOT NULL,
    type              ENUM('Editorial', 'Algorithm', 'User') NOT NULL,
    p_platform_id     INT NOT NULL,
    CONSTRAINT fk_p_platform_id
    FOREIGN KEY (p_platform_id) REFERENCES platform(platform_id)
);

CREATE TABLE `release` (
    rel_id           INT AUTO_INCREMENT PRIMARY KEY,
    title            VARCHAR(255) NOT NULL,
    type             ENUM('Album', 'Single', 'EP', 'Compilation'),
    status           ENUM('Processing', 'Approved', 'Released', 'Takedown'),
    release_date     DATETIME NOT NULL,
    release_artist_id INT NOT NULL,
    CONSTRAINT fk_release_artist_id
    FOREIGN KEY (release_artist_id) REFERENCES artist(artist_id)
    ON DELETE CASCADE
);

CREATE TABLE manages (
    manages_user_id    INT NOT NULL,
    manages_artist_id  INT NOT NULL,
    PRIMARY KEY(manages_user_id, manages_artist_id),
    CONSTRAINT fk_manages_user_id
    FOREIGN KEY (manages_user_id) REFERENCES user(user_id),
    CONSTRAINT fk_manages_artist_id
    FOREIGN KEY (manages_artist_id) REFERENCES artist(artist_id)
);

CREATE TABLE track (
    track_id          INT AUTO_INCREMENT PRIMARY KEY,
    title             VARCHAR(255) NOT NULL,
    genre             VARCHAR(50) NOT NULL,
    isrc_code         VARCHAR(12) NOT NULL,
    track_artist_id   INT NOT NULL,
    track_release_id  INT NOT NULL,
    CONSTRAINT fk_track_artist_id
    FOREIGN KEY (track_artist_id) REFERENCES artist(artist_id)
    ON DELETE CASCADE,
    CONSTRAINT fk_track_release_id
    FOREIGN KEY (track_release_id) REFERENCES `release`(rel_id)
    ON DELETE CASCADE
);

CREATE TABLE financialReport (
    freport_id       INT AUTO_INCREMENT PRIMARY KEY,
    start_period     DATETIME NOT NULL,
    end_period       DATETIME NOT NULL,
    fr_release_id    INT NOT NULL,
    CONSTRAINT fk_fr_release_id
    FOREIGN KEY (fr_release_id) REFERENCES `release`(rel_id)
);

CREATE TABLE asset (
    asset_id            INT AUTO_INCREMENT PRIMARY KEY,
    file_url            VARCHAR(255) NOT NULL,
    file_type           ENUM('Audio','Artwork', 'Credits'),
    upload_status       TINYINT(1),
    asset_release_id    INT NOT NULL,
    CONSTRAINT fk_asset_release_id
    FOREIGN KEY (asset_release_id) REFERENCES `release`(rel_id)
    ON DELETE CASCADE
);

CREATE TABLE payoutProfiles (
    payout_id         INT AUTO_INCREMENT PRIMARY KEY,
    collab_email      VARCHAR(255) NOT NULL,
    role              VARCHAR(50) NOT NULL,
    split_percentage  DECIMAL(5,2),
    pp_release_id     INT NOT NULL,
    CONSTRAINT fk_pp_release_id
    FOREIGN KEY (pp_release_id) REFERENCES `release`(rel_id)
);

CREATE TABLE streamEvent (
    event_id         INT AUTO_INCREMENT PRIMARY KEY,
    time_stamp       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_skipped       TINYINT(1) NOT NULL,
    rev_generated    DECIMAL(19,4) NOT NULL,
    event_listener_id INT NULL,
    event_track_id    INT NOT NULL,
    event_platform_id INT NOT NULL,
    event_location_id INT NOT NULL,
    CONSTRAINT fk_event_listener_id
    FOREIGN KEY (event_listener_id) REFERENCES listener(listener_id)
    ON DELETE SET NULL,
    CONSTRAINT fk_event_track_id
    FOREIGN KEY (event_track_id) REFERENCES track(track_id)
    ON DELETE RESTRICT,
    CONSTRAINT fk_event_platform_id
    FOREIGN KEY (event_platform_id) REFERENCES platform(platform_id),
    CONSTRAINT fk_event_location_id
    FOREIGN KEY (event_location_id) REFERENCES location(location_id)
);

CREATE TABLE playlistEvent (
    pt_event_id INT NOT NULL,
    pt_playlist_id INT NOT NULL,
    PRIMARY KEY(pt_event_id, pt_playlist_id),
    CONSTRAINT fk_pt_event_id
    FOREIGN KEY (pt_event_id) REFERENCES streamEvent(event_id)
    ON DELETE CASCADE,
    CONSTRAINT fk_pt_playlist_id
    FOREIGN KEY (pt_playlist_id) REFERENCES playlist(playlist_id)
);