.PHONY: publish
publish:
	uv build --clear && uv publish
