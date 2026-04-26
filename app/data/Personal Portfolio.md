---
title: Personal Portfolio
slug: personal-portfolio
tagline: Flask-based platform as a container of my works.
thumbnail_url: https://cdn.pixabay.com/photo/2018/02/22/18/21/laptop-3173613_1280.png
hero_url: https://cdn.pixabay.com/photo/2015/10/27/14/40/programming-1009134_1280.jpg
hero_alt: terminal-hero
start_date: 2026-01-03
---

## Personal Portfolio
Flask-based platform as a container of my workflow.

## Overview
The project originated from a need for centralized 'single-source' for my personal identity, a platform that reflecting my journey as a whole. Functioning as a live 'patch log' to document my growth. 

This is actually my first flask application. The development process idea is just start simple and refactor for complexity later.

## Details
- Build on Flask (**Python**) micro-framework, utilizing a modular routing system to handle dynamic content delivery.
The application follow 'Logic-first' design, prioritizing server-side stability and clean data structure before scaling to complex database integration.
By building from scratch, I am learning the manual orchestration of routing logic and server-side state management.
- Jinja2 template engine is used to inject structured data into html templates instead of hardcoding every pages.
- This teaches me how to deliver back-end Python logic into front-end presentation.
- Data entries are stored in json and seeded into SQLite, mirorring the real-world database design.
SQLAlchemy is used as Object Relational Mapper (ORM) to map each stored data into Python Objects.
- The UI is utilizing CSS Bootstrap with slight custom css to make a clean and tidy look.